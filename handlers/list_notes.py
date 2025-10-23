from telegram import Update
from telegram.ext import (
                          ContextTypes,
                          )
from data.database import get_notes


async def list_notes(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    notes = get_notes(user_id)
    if not notes:
        await update.message.reply_text("У тебя пока нет заметок.")
        return
    response = "\n\n".join(
        [f"{note[0]}. {note[1]} (🕒 {note[2][:16]})" for note in notes]
    )
    await update.message.reply_text(response)