"""
Handler for the /list command in the Telegram bot.

This module defines an asynchronous handler function that lists all
notes for the current user. Includes logging and error handling.
"""

from typing import Awaitable
from telegram import Update
from telegram.ext import ContextTypes
from data.database import get_notes
from utils.logger import logger


async def list_notes(update: Update, context: ContextTypes.DEFAULT_TYPE) -> Awaitable[None]:
    """
    Handle the /list command from the user.

    Behavior:
      - Retrieves all notes of the user using get_notes().
      - Formats and sends the list of notes with IDs and creation time.
      - Logs the action and handles any database errors.

    Args:
        update (telegram.Update): Incoming Telegram update object.
        context (telegram.ext.ContextTypes.DEFAULT_TYPE): Context of the command.

    Returns:
        Awaitable[None]: Sends a message with the list of notes to the user.
    """
    user = update.effective_user
    user_id = user.id if user else None

    try:
        notes = get_notes(user_id)
        if not notes:
            await update.message.reply_text("You don't have any notes yet.")
            logger.info(f"/list: no notes for user_id={user_id}")
            return

        response = "\n\n".join(
            [f"{note[0]}. {note[1]} (🕒 {note[2][:16]})" for note in notes]
        )
        await update.message.reply_text(response)
        logger.info(f"/list: sent {len(notes)} notes to user_id={user_id}")
    except Exception as e:
        await update.message.reply_text("❌ Error occurred while fetching notes.")
        logger.error(f"Error listing notes for user_id={user_id}: {e}", exc_info=True)
