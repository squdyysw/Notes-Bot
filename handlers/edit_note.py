"""
Handler for the /edit command in the Telegram bot.

Allows the user to edit an existing note using its visual index from /list.
Includes logging and error handling.
"""

from typing import Awaitable
from telegram import Update
from telegram.ext import ContextTypes
from data.database import update_note
from utils.logger import logger
from handlers.list_notes import USER_INDEX_MAP

async def edit(update: Update, context: ContextTypes.DEFAULT_TYPE) -> Awaitable[None]:
    """
    Handle the /edit command from the user.

    Behavior:
      - Reads the note number (visual index) from command arguments.
      - Validates input and prompts if invalid.
      - Requests new text from the user.
      - Updates the note using update_note() from database.

    Args:
        update (telegram.Update): Incoming Telegram update object.
        context (telegram.ext.ContextTypes.DEFAULT_TYPE): Context with command arguments.

    Returns:
        Awaitable[None]: Sends feedback to the user.
    """
    user = update.effective_user
    user_id = user.id if user else None
    if not user_id:
        return

    if not context.args:
        await update.message.reply_text("Use: /edit <note number>")
        logger.debug(f"/edit: missing note number from user_id={user_id}")
        return

    try:
        visual_idx = int(context.args[0])
    except ValueError:
        await update.message.reply_text("Note number must be a number.")
        logger.debug(f"/edit: invalid note number '{context.args[0]}' from user_id={user_id}")
        return

    real_id = USER_INDEX_MAP.get(user_id, {}).get(visual_idx)
    if not real_id:
        await update.message.reply_text("Note not found. Make sure you used /list recently.")
        logger.warning(f"/edit: no mapping for visual_idx={visual_idx} user_id={user_id}")
        return

    await update.message.reply_text("Please enter the new text for the note:")

    # Handler to capture the next message from the user
    async def receive_new_text(msg_update: Update, msg_context: ContextTypes.DEFAULT_TYPE):
        new_text = msg_update.message.text.strip()
        if not new_text:
            await msg_update.message.reply_text("❌ Empty text. Edit cancelled.")
            return
        try:
            if update_note(user_id, real_id, new_text):
                await msg_update.message.reply_text(f"✅ Note {visual_idx} updated.")
            else:
                await msg_update.message.reply_text("❌ Note not found or could not be updated.")
        except Exception as e:
            await msg_update.message.reply_text("❌ Error occurred while updating note.")
            logger.error(f"Error updating note_id={real_id} for user_id={user_id}: {e}", exc_info=True)

        # Remove the handler after receiving one message
        msg_context.application.remove_handler(handler)

    from telegram.ext import MessageHandler, filters
    handler = MessageHandler(filters.TEXT & ~filters.COMMAND, receive_new_text)
    context.application.add_handler(handler)