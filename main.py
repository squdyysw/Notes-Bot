import logging
from telegram.ext import Application, CommandHandler
from data.database import init_db
from handlers.add_note import add
from handlers.list_notes import list_notes
from handlers.delete_note import delete
from handlers.start import start
from handlers.help import help_command
from handlers.find_note import find
from config import TOKEN

logging.basicConfig(level=logging.INFO)


def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("add", add))
    app.add_handler(CommandHandler("list", list_notes))
    app.add_handler(CommandHandler("delete", delete))
    app.add_handler(CommandHandler("find", find))

    print("✅ Бот запущен...")
    init_db()
    app.run_polling()


if __name__ == "__main__":
    main()
