"""
Handler for the /add command in the Telegram bot.

This module defines an asynchronous handler function that allows users
to add text notes. The note is saved to the database and confirmed to the user.
Includes logging and error handling.
"""

from typing import Awaitable
from telegram import Update
from telegram.ext import ContextTypes
from data.database import add_note
from utils.logger import logger


async def add(update: Update, context: ContextTypes.DEFAULT_TYPE) -> Awaitable[None]:
    """
    Handle the /add command from the user.

    Behavior:
      - Reads the note text from command arguments (/add <text>).
      - Validates input and informs the user if it's empty.
      - Saves the note to the database.
      - Logs successful and failed operations.

    Args:
        update (telegram.Update): The incoming Telegram update object.
        context (telegram.ext.ContextTypes.DEFAULT_TYPE): Context with command arguments.

    Returns:
        Awaitable[None]: Does not return anything, sends messages to the user.
    """
    user = update.effective_user
    user_id = user.id if user else None
    note_text = " ".join(context.args).strip()

    if not note_text:
        await update.message.reply_text("Use: /add <note text>")
        logger.debug(f"/add: empty note text from user_id={user_id}")
        return

    try:
        add_note(user_id, note_text)
        await update.message.reply_text("✅ Note saved!")
        logger.info(f"Note added for user_id={user_id}: {note_text[:50]!r}")
    except Exception as e:
        logger.error(f"Error adding note for user_id={user_id}: {e}", exc_info=True)
        await update.message.reply_text("❌ An error occurred while saving your note.")