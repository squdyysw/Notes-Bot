"""
Handler for the /delete command in the Telegram bot.

This module defines an asynchronous handler function that deletes a note
by its ID for the current user. Includes logging and error handling.
"""

from typing import Awaitable
from telegram import Update
from telegram.ext import ContextTypes
from data.database import delete_note
from utils.logger import logger


async def delete(update: Update, context: ContextTypes.DEFAULT_TYPE) -> Awaitable[None]:
    """
    Handle the /delete command from the user.

    Behavior:
      - Reads the note ID from command arguments (/delete <note_id>).
      - Validates input and informs the user if invalid.
      - Deletes the note using delete_note() from database.
      - Sends feedback to the user and logs actions/errors.

    Args:
        update (telegram.Update): Incoming Telegram update object.
        context (telegram.ext.ContextTypes.DEFAULT_TYPE): Context with command arguments.

    Returns:
        Awaitable[None]: Does not return anything, sends messages to the user.
    """
    user = update.effective_user
    user_id = user.id if user else None

    if not context.args:
        await update.message.reply_text("Use: /delete <note ID>")
        logger.debug(f"/delete: missing note ID from user_id={user_id}")
        return

    try:
        note_id = int(context.args[0])
    except ValueError:
        await update.message.reply_text("Note ID must be a number.")
        logger.debug(f"/delete: invalid note ID '{context.args[0]}' from user_id={user_id}")
        return

    try:
        deleted = delete_note(note_id, user_id)
        if deleted:
            await update.message.reply_text("🗑️ Note deleted.")
            logger.info(f"Deleted note_id={note_id} for user_id={user_id}")
        else:
            await update.message.reply_text("🗑️ Note not found.")
            logger.warning(f"Attempted to delete non-existent note_id={note_id} for user_id={user_id}")
    except Exception as e:
        await update.message.reply_text("❌ Error occurred while deleting note.")
        logger.error(f"Error deleting note_id={note_id} for user_id={user_id}: {e}", exc_info=True)