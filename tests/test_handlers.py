import pytest
from telegram import User, Message, Update
from telegram.ext import ContextTypes
from unittest.mock import AsyncMock
from handlers.add_note import add_note as add_handler
from handlers.list_notes import list_notes as list_handler
from handlers.delete_note import delete_note as delete_handler
from data import database

@pytest.mark.asyncio
async def test_add_handler():
    database.DB_PATH = ":memory:"
    database.init_db()

    user = User(id=1, first_name="TestUser", is_bot=False)
    message = AsyncMock(spec=Message)
    message.reply_text = AsyncMock()
    update = Update(update_id=1, message=message, effective_user=user)

    context = AsyncMock(spec=ContextTypes.DEFAULT_TYPE)
    context.args = ["Test note"]
    context.application = AsyncMock()

    await add_handler.add(update, context)

    notes = database.get_notes(user.id)
    assert len(notes) == 1
    assert notes[0][1] == "Test note"
    message.reply_text.assert_called_with("✅ Note saved!")

@pytest.mark.asyncio
async def test_list_handler():
    database.DB_PATH = ":memory:"
    database.init_db()

    user_id = 2
    database.add_note(user_id, "Note 1")
    database.add_note(user_id, "Note 2")

    user = User(id=user_id, first_name="ListUser", is_bot=False)
    message = AsyncMock(spec=Message)
    message.reply_text = AsyncMock()
    update = Update(update_id=2, message=message, effective_user=user)

    context = AsyncMock(spec=ContextTypes.DEFAULT_TYPE)

    await list_handler.list_notes(update, context)
    message.reply_text.assert_called()
    # Можно дополнительно проверить текст вызова, но тут базовая проверка

@pytest.mark.asyncio
async def test_delete_handler():
    database.DB_PATH = ":memory:"
    database.init_db()

    user_id = 3
    database.add_note(user_id, "Note to delete")
    note_id = database.get_notes(user_id)[0][0]

    user = User(id=user_id, first_name="DeleteUser", is_bot=False)
    message = AsyncMock(spec=Message)
    message.reply_text = AsyncMock()
    update = Update(update_id=3, message=message, effective_user=user)

    context = AsyncMock(spec=ContextTypes.DEFAULT_TYPE)
    context.args = [str(note_id)]
    context.application = AsyncMock()

    await delete_handler.delete(update, context)
    message.reply_text.assert_called_with("🗑️ Note deleted.")
    assert database.get_notes(user_id) == []
