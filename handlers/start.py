from telegram import Update
from telegram.ext import (
                          ContextTypes,
                          )


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет! Я твой бот для заметок.\n\n"
                                    "Команды:\n"
                                    "/add <текст> — добавить заметку\n"
                                    "/list — показать все\n"
                                    "/delete <номер> — удалить\n"
                                    "/find <слово> — поиск")