"""
Handler for the /add command in the Telegram bot.

This module defines an asynchronous handler function that allows users
to add text notes. Supports immediate note after command or waiting for
user input in a new message. Includes logging and error handling.
"""

from typing import Awaitable
from telegram import Update
from telegram.ext import ContextTypes, MessageHandler, filters
from data.database import add_note
from utils.logger import logger


async def add(update: Update, context: ContextTypes.DEFAULT_TYPE) -> Awaitable[None]:
    """
    Handle the /add command from the user.

    Behavior:
      - If text is provided with the command, save immediately.
      - If no text, prompt the user to send the note in a new message.
      - Logs successful and failed operations.

    Args:
        update (telegram.Update): Incoming Telegram update object.
        context (telegram.ext.ContextTypes.DEFAULT_TYPE): Context with command arguments.

    Returns:
        Awaitable[None]: Sends messages to the user.
    """
    user = update.effective_user
    user_id = user.id if user else None
    note_text = " ".join(context.args).strip()

    if note_text:
        try:
            add_note(user_id, note_text)
            await update.message.reply_text("✅ Note saved!")
            logger.info(f"Note added for user_id={user_id}: {note_text[:50]!r}")
        except Exception as e:
            logger.error(f"Error adding note for user_id={user_id}: {e}", exc_info=True)
            await update.message.reply_text("❌ An error occurred while saving your note.")
        return

    # If no text, prompt user to send message
    await update.message.reply_text("Please enter your note text:")

    async def receive_note(msg_update: Update, msg_context: ContextTypes.DEFAULT_TYPE):
        new_note = msg_update.message.text.strip()
        if not new_note:
            await msg_update.message.reply_text("❌ Empty note. Cancelled.")
            return
        try:
            add_note(user_id, new_note)
            await msg_update.message.reply_text("✅ Note saved!")
            logger.info(f"Note added for user_id={user_id}: {new_note[:50]!r}")
        except Exception as e:
            logger.error(f"Error adding note for user_id={user_id}: {e}", exc_info=True)
            await msg_update.message.reply_text("❌ An error occurred while saving your note.")
        msg_context.application.remove_handler(handler)

    handler = MessageHandler(filters.TEXT & ~filters.COMMAND, receive_note)
    context.application.add_handler(handler)