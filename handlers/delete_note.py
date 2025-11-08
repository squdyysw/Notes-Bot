"""
Handler for the /delete command in the Telegram bot.

Deletes a note by its visual index as shown in /list.
"""

from typing import Awaitable
from telegram import Update
from telegram.ext import ContextTypes
from data.database import delete_note
from utils.logger import logger
from handlers.list_notes import USER_INDEX_MAP

async def delete(update: Update, context: ContextTypes.DEFAULT_TYPE) -> Awaitable[None]:
    """
    Handle the /delete command from the user using visual numbering.

    Args:
        update (telegram.Update): Incoming Telegram update object.
        context (telegram.ext.ContextTypes.DEFAULT_TYPE): Context of the command.

    Returns:
        Awaitable[None]: Sends feedback to the user.
    """
    user = update.effective_user
    user_id = user.id if user else None
    if not user_id:
        return

    if not context.args:
        await update.message.reply_text("Use: /delete <note number>")
        logger.debug(f"/delete: missing note number from user_id={user_id}")
        return

    try:
        visual_idx = int(context.args[0])
    except ValueError:
        await update.message.reply_text("Note number must be a number.")
        logger.debug(f"/delete: invalid note number '{context.args[0]}' from user_id={user_id}")
        return

    real_id = USER_INDEX_MAP.get(user_id, {}).get(visual_idx)
    if not real_id:
        await update.message.reply_text("🗑️ Note not found. Make sure you used /list recently.")
        logger.warning(f"/delete: no mapping for visual_idx={visual_idx} user_id={user_id}")
        return

    try:
        deleted = delete_note(real_id, user_id)
        if deleted:
            await update.message.reply_text(f"🗑️ Note {visual_idx} deleted.")
            logger.info(f"Deleted note_id={real_id} (visual {visual_idx}) for user_id={user_id}")
            # Update mapping after deletion
            USER_INDEX_MAP[user_id].pop(visual_idx)
        else:
            await update.message.reply_text("🗑️ Note not found.")
            logger.warning(f"Attempted to delete non-existent note_id={real_id} for user_id={user_id}")
    except Exception as e:
        await update.message.reply_text("❌ Error occurred while deleting note.")
        logger.error(f"Error deleting note_id={real_id} for user_id={user_id}: {e}", exc_info=True)