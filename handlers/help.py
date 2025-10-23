from telegram import Update
from telegram.ext import (
                          ContextTypes,
                          )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Доступные команды:\n"
                                    "/add <текст> — добавить заметку\n"
                                    "/list — показать все\n"
                                    "/delete <номер> — удалить\n"
                                    "/find <слово> — поиск")