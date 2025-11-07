"""
Handler for the /find command in the Telegram bot.

This module defines an asynchronous handler function that searches
notes for a specific keyword for the current user. Includes logging
and error handling.
"""

from typing import Awaitable
from telegram import Update
from telegram.ext import ContextTypes
from data.database import find_notes
from utils.logger import logger


async def find(update: Update, context: ContextTypes.DEFAULT_TYPE) -> Awaitable[None]:
    """
    Handle the /find command from the user.

    Behavior:
      - Reads a search keyword from command arguments (/find <keyword>).
      - Searches the user's notes containing the keyword using find_notes().
      - Sends the results to the user and logs the operation.

    Args:
        update (telegram.Update): Incoming Telegram update object.
        context (telegram.ext.ContextTypes.DEFAULT_TYPE): Context with command arguments.

    Returns:
        Awaitable[None]: Does not return anything, sends messages to the user.
    """
    user = update.effective_user
    user_id = user.id if user else None

    if not context.args:
        await update.message.reply_text("Use: /find <keyword>")
        logger.debug(f"/find: missing keyword from user_id={user_id}")
        return

    keyword = " ".join(context.args).strip()

    try:
        results = find_notes(user_id, keyword)
        if not results:
            await update.message.reply_text("🔍 Nothing found.")
            logger.info(f"/find: no results for keyword='{keyword}' from user_id={user_id}")
            return

        response = "\n\n".join([f"📝 {note[1]}" for note in results])
        await update.message.reply_text(f"Found:\n\n{response}")
        logger.info(f"/find: found {len(results)} results for keyword='{keyword}' from user_id={user_id}")
    except Exception as e:
        await update.message.reply_text("❌ Error occurred while searching notes.")
        logger.error(f"Error finding notes for user_id={user_id} with keyword='{keyword}': {e}", exc_info=True)