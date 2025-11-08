"""
Handler for the /list command in the Telegram bot.

This module defines an asynchronous handler function that lists all
notes for the current user. Includes logging, date formatting,
and robust error handling.
"""

from typing import Awaitable
from datetime import datetime
from telegram import Update
from telegram.ext import ContextTypes
from data.database import get_notes
from utils.logger import logger

# Store index-to-ID mapping for each user in memory
USER_INDEX_MAP = {}

async def list_notes(update: Update, context: ContextTypes.DEFAULT_TYPE) -> Awaitable[None]:
    """
    Handle the /list command from the user.

    Behavior:
      - Retrieves all notes of the user using get_notes().
      - Displays notes with sequential numbering (1, 2, 3, ...).
      - Formats creation dates as DD.MM.YYYY HH:MM.
      - Stores mapping index->real_id for deletion.
      - Logs and handles any errors.

    Args:
        update (telegram.Update): Incoming Telegram update object.
        context (telegram.ext.ContextTypes.DEFAULT_TYPE): Context of the command.

    Returns:
        Awaitable[None]: Sends a formatted list of notes to the user.
    """
    user = update.effective_user
    user_id = user.id if user else None
    if not user_id:
        return

    try:
        notes = get_notes(user_id)
        if not notes:
            await update.message.reply_text("You don't have any notes yet.")
            logger.info(f"/list: no notes for user_id={user_id}")
            USER_INDEX_MAP[user_id] = {}
            return

        index_map = {}
        formatted_notes = []

        for idx, (real_id, text, created_at) in enumerate(notes, start=1):
            index_map[idx] = real_id
            try:
                dt = datetime.fromisoformat(created_at)
                formatted_date = dt.strftime("%d.%m.%Y %H:%M")
            except ValueError:
                formatted_date = created_at[:16]

            formatted_notes.append(f"{idx}. {text}\n🕒 {formatted_date}")

        response = "\n\n".join(formatted_notes)
        await update.message.reply_text(response)
        logger.info(f"/list: sent {len(notes)} notes to user_id={user_id}")

        # Save mapping for deletion
        USER_INDEX_MAP[user_id] = index_map

    except Exception as e:
        await update.message.reply_text("❌ An error occurred while fetching your notes.")
        logger.error(f"Error listing notes for user_id={user_id}: {e}", exc_info=True)