from telegram import Update
from telegram.ext import ContextTypes
from data.database import find_notes

async def find(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if not context.args:
        await update.message.reply_text("Используй: /find <слово для поиска>")
        return

    keyword = " ".join(context.args)
    results = find_notes(user_id, keyword)

    if not results:
        await update.message.reply_text("🔍 Ничего не найдено.")
        return

    response = "\n\n".join([f"📝 {note[1]}" for note in results])
    await update.message.reply_text(f"Найдено:\n\n{response}")
