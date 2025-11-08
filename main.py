import logging
from telegram.ext import Application, CommandHandler
from data.database import init_db
from handlers.add_note import add
from handlers.list_notes import list_notes
from handlers.delete_note import delete
from handlers.start import start
from handlers.help import help_command
from handlers.find_note import find
from handlers.edit_note import edit
from config import TOKEN

# Настройка базового логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def main():
    # Инициализация приложения Telegram
    app = Application.builder().token(TOKEN).build()

    # Инициализация базы данных
    init_db()

    # Регистрация команд
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("add", add))
    app.add_handler(CommandHandler("list", list_notes))
    app.add_handler(CommandHandler("delete", delete))
    app.add_handler(CommandHandler("find", find))
    app.add_handler(CommandHandler("edit", edit))  # новая команда /edit

    print("✅ Bot started...")
    app.run_polling()


if __name__ == "__main__":
    main()
