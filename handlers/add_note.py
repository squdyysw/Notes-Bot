from telegram import Update
from telegram.ext import (
                          ContextTypes,
                          )
from data.database import add_note


async def add(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    note_text = " ".join(context.args)
    if not note_text:
        await update.message.reply_text("Используй: /add <текст заметки>")
        return
    add_note(user_id, note_text)
    await update.message.reply_text("✅ Заметка сохранена!")