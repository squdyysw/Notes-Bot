import pytest
import asyncio
from unittest.mock import AsyncMock, MagicMock
from datetime import datetime
from data.database import add_note, get_notes, delete_note
from handlers.add_note import add_note
from handlers.list_notes import list_notes
from handlers.edit_note import edit  # если у тебя отдельный файл

# ------------------------------
# Fixtures
# ------------------------------
@pytest.fixture
def mock_update():
    """Mock Telegram Update object"""
    update = AsyncMock()
    update.effective_user.id = 12345
    update.message.reply_text = AsyncMock()
    return update

@pytest.fixture
def mock_context():
    """Mock Telegram Context object"""
    context = AsyncMock()
    context.args = []
    context.application.add_handler = MagicMock()
    context.application.remove_handler = MagicMock()
    return context

# ------------------------------
# Tests for /add command
# ------------------------------
@pytest.mark.asyncio
async def test_add_with_text(mock_update, mock_context):
    """Test /add command with immediate text"""
    mock_context.args = ["Test note"]
    await add(mock_update, mock_context)
    mock_update.message.reply_text.assert_called_with("✅ Note saved!")

@pytest.mark.asyncio
async def test_add_without_text(mock_update, mock_context):
    """Test /add command with delayed note entry"""
    mock_context.args = []
    await add(mock_update, mock_context)
    mock_update.message.reply_text.assert_called_with("Please enter your note text:")

# ------------------------------
# Tests for /list command
# ------------------------------
@pytest.mark.asyncio
async def test_list_notes_empty(mock_update, mock_context):
    """Test /list when user has no notes"""
    # Ensure no notes exist for this user
    for note in get_notes(12345):
        delete_note(note[0], 12345)
    from handlers.list_notes import list_notes
    await list_notes(mock_update, mock_context)
    mock_update.message.reply_text.assert_called_with("You don't have any notes yet.")

@pytest.mark.asyncio
async def test_list_notes_with_notes(mock_update, mock_context):
    """Test /list with existing notes"""
    add_note(12345, "Note 1")
    add_note(12345, "Note 2")
    await list_notes(mock_update, mock_context)
    # Check that reply_text contains "1. Note 1" and "2. Note 2"
    called_text = mock_update.message.reply_text.call_args[0][0]
    assert "1. Note 1" in called_text
    assert "2. Note 2" in called_text

# ------------------------------
# Tests for /edit command
# ------------------------------
@pytest.mark.asyncio
async def test_edit_note_functionality(mock_update, mock_context):
    """Test editing an existing note"""
    # First add a note
    add_note(12345, "Original note")
    notes = get_notes(12345)
    note_id = notes[0][0]

    # Simulate edit command
    mock_context.args = [str(note_id), "Updated note"]
    await edit_note(mock_update, mock_context)
    mock_update.message.reply_text.assert_called_with("✏️ Note updated!")

    # Check the database
    updated_note = get_notes(12345)[0][1]
    assert updated_note == "Updated note"
