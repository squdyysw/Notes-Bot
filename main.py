"""
Main entry point for the Telegram notes bot.

This module initializes the bot, registers command handlers,
and starts polling. Also initializes the database.
"""

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
from utils.logger import logger


def main():
    """
    Initialize the bot application, register handlers, and start polling.
    """
    try:
        app = Application.builder().token(TOKEN).build()

        # Register command handlers
        app.add_handler(CommandHandler("start", start))
        app.add_handler(CommandHandler("help", help_command))
        app.add_handler(CommandHandler("add", add))
        app.add_handler(CommandHandler("list", list_notes))
        app.add_handler(CommandHandler("delete", delete))
        app.add_handler(CommandHandler("find", find))

        # Initialize database
        init_db()
        logger.info("Database initialized successfully.")

        # Start bot polling
        logger.info("✅ Bot started...")
        print("✅ Bot started...")
        app.run_polling()
    except Exception as e:
        logger.critical(f"Critical error in main(): {e}", exc_info=True)
        print(f"❌ Critical error: {e}")


if __name__ == "__main__":
    main()