import sqlite3
from datetime import datetime
from config import DB_PATH
from utils.logger import logger


def init_db():
    """
    Initializes the SQLite database and creates the 'notes' table if it doesn't exist.
    """
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS notes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            text TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
        """)
        conn.commit()
        logger.info("Database initialized successfully.")
    except sqlite3.Error as e:
        logger.error(f"Database initialization failed: {e}")
    finally:
        conn.close()


def add_note(user_id: int, text: str) -> None:
    """
    Adds a new note for a specific user.

    Args:
        user_id (int): Telegram user ID.
        text (str): Text content of the note.
    """
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO notes (user_id, text, created_at) VALUES (?, ?, ?)",
            (user_id, text, datetime.now().isoformat())
        )
        conn.commit()
        logger.info(f"Note added for user_id={user_id}.")
    except sqlite3.Error as e:
        logger.error(f"Error adding note for user_id={user_id}: {e}")
    finally:
        conn.close()


def get_notes(user_id: int):
    """
    Retrieves all notes belonging to a specific user.

    Args:
        user_id (int): Telegram user ID.

    Returns:
        list[tuple[int, str, str]]: List of notes as tuples (id, text, created_at).
    """
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute(
            "SELECT id, text, created_at FROM notes WHERE user_id = ? ORDER BY id ASC",
            (user_id,)
        )
        rows = cursor.fetchall()
        logger.info(f"Fetched {len(rows)} notes for user_id={user_id}.")
        return rows
    except sqlite3.Error as e:
        logger.error(f"Error fetching notes for user_id={user_id}: {e}")
        return []
    finally:
        conn.close()


def delete_note(note_id: int, user_id: int) -> bool:
    """
    Deletes a note by its ID for a specific user.

    Args:
        note_id (int): Note ID in the database.
        user_id (int): Telegram user ID.

    Returns:
        bool: True if a note was deleted, False otherwise.
    """
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute(
            "DELETE FROM notes WHERE id = ? AND user_id = ?",
            (note_id, user_id)
        )
        conn.commit()
        deleted = cursor.rowcount > 0
        if deleted:
            logger.info(f"Deleted note_id={note_id} for user_id={user_id}.")
        else:
            logger.warning(f"No note found for deletion: note_id={note_id}, user_id={user_id}.")
        return deleted
    except sqlite3.Error as e:
        logger.error(f"Error deleting note_id={note_id} for user_id={user_id}: {e}")
        return False
    finally:
        conn.close()


def find_notes(user_id: int, keyword: str):
    """
    Searches for notes containing a keyword for a specific user.

    Args:
        user_id (int): Telegram user ID.
        keyword (str): Keyword to search for in note texts.

    Returns:
        list[tuple[int, str]]: List of matching notes as tuples (id, text).
    """
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute(
            "SELECT id, text FROM notes WHERE user_id = ? AND text LIKE ?",
            (user_id, f"%{keyword}%")
        )
        results = cursor.fetchall()
        logger.info(f"Found {len(results)} notes for user_id={user_id} with keyword='{keyword}'.")
        return results
    except sqlite3.Error as e:
        logger.error(f"Error searching notes for user_id={user_id} with keyword='{keyword}': {e}")
        return []
    finally:
        conn.close()
