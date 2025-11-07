"""
Handler for the /start command in the Telegram bot.

This module defines an asynchronous handler function that welcomes
the user and provides initial instructions. Includes logging.
"""

from typing import Awaitable
from telegram import Update
from telegram.ext import ContextTypes
from utils.logger import logger


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> Awaitable[None]:
    """
    Handle the /start command from the user.

    Behavior:
      - Sends a welcome message and a list of available bot commands.
      - Logs the use of the command.

    Args:
        update (telegram.Update): Incoming Telegram update object.
        context (telegram.ext.ContextTypes.DEFAULT_TYPE): Context of the command.

    Returns:
        Awaitable[None]: Sends a message to the user.
    """
    try:
        await update.message.reply_text(
            "Hello! I'm your notes bot.\n\n"
            "Commands:\n"
            "/add <text> — add a note\n"
            "/list — show all notes\n"
            "/delete <ID> — delete a note\n"
            "/find <keyword> — search notes"
        )
        user = update.effective_user
        user_id = user.id if user else None
        logger.info(f"/start command used by user_id={user_id}")
    except Exception as e:
        await update.message.reply_text("❌ Error occurred while starting the bot.")
        logger.error(f"Error in /start command for user_id={user_id}: {e}", exc_info=True)