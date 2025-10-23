from telegram import Update
from telegram.ext import (
                          ContextTypes,
                          )
from data.database import delete_note


async def delete(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if not context.args:
        await update.message.reply_text("Используй: /delete <id заметки>")
        return
    try:
        note_id = int(context.args[0])
    except ValueError:
        await update.message.reply_text("ID заметки должно быть числом.")
        return
    delete_note(note_id, user_id)
    await update.message.reply_text("🗑️ Заметка удалена (если существовала).")
