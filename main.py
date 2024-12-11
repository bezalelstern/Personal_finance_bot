import asyncio
import logging
from telegram._update import Update
from telegram.ext import Application, ContextTypes
from repository.postgres_repo import setup_database
from telegram_repository.handlers import register_handlers
from telegram_repository.main_repo import start

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)
logging.getLogger("httpx").setLevel(logging.WARNING)
logging.getLogger("telegram").setLevel(logging.WARNING)

def main() -> None:
    """Run the bot."""
    setup_database()
    print("Bot is running")
    application = Application.builder().token('7349809392:AAHRKfATE1rMImHVejkOeF1Y9afAZz4HE6w').build()
    register_handlers(application)
    try:
        application.run_polling(allowed_updates=Update.ALL_TYPES)
    except Exception as e:
        logger.error(f"An error occurred: {e}")

#הרצה
if __name__ == '__main__':
    main()




