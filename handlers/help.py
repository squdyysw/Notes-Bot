from typing import Awaitable
from telegram import Update
from telegram.ext import ContextTypes
from utils.logger import logger


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> Awaitable[None]:
    """
    Handle the /help command from the user.

    Behavior:
      - Sends a list of available bot commands and their descriptions.
      - Logs the action.

    Args:
        update (telegram.Update): Incoming Telegram update object.
        context (telegram.ext.ContextTypes.DEFAULT_TYPE): Context of the command.

    Returns:
        Awaitable[None]: Does not return anything, sends messages to the user.
    """
    try:
        await update.message.reply_text(
            "Available commands:\n"
            "/add <text> — add a note or input after command\n"
            "/list — show all notes\n"
            "/delete <ID> — delete a note\n"
            "/find <keyword> — search notes\n"
            "/edit <number> — edit a note"
        )
        user = update.effective_user
        user_id = user.id if user else None
        logger.info(f"/help command used by user_id={user_id}")
    except Exception as e:
        await update.message.reply_text("❌ Error occurred while showing help.")
        logger.error(f"Error in /help command for user_id={user_id}: {e}", exc_info=True)
