import pytest
from data.database import add_note

@pytest.fixture
def init_test_db(tmp_path):
    """Initialize a temporary database for testing."""
    database.DB_PATH = tmp_path / "test_notes.db"
    database.init_db()
    return database

def test_add_and_get_notes(init_test_db):
    db = init_test_db
    user_id = 1
    db.add_note(user_id, "Test note 1")
    db.add_note(user_id, "Test note 2")

    notes = db.get_notes(user_id)
    assert len(notes) == 2
    assert notes[0][1] == "Test note 1"
    assert notes[1][1] == "Test note 2"

def test_delete_note_success(init_test_db):
    db = init_test_db
    user_id = 2
    db.add_note(user_id, "To delete")
    note_id = db.get_notes(user_id)[0][0]

    deleted = db.delete_note(note_id, user_id)
    assert deleted is True
    assert db.get_notes(user_id) == []

def test_delete_note_fail(init_test_db):
    db = init_test_db
    user_id = 3
    deleted = db.delete_note(999, user_id)
    assert deleted is False

def test_find_notes(init_test_db):
    db = init_test_db
    user_id = 4
    db.add_note(user_id, "Find me")
    db.add_note(user_id, "Don't find me")

    results = db.find_notes(user_id, "Find")
    assert len(results) == 1
    assert "Find me" in results[0][1]
