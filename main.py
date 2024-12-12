import logging
from telegram._update import Update
from telegram.ext import Application
from repository.postgres_repo import setup_database
from telegram_repository.handlers import register_handlers

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)
logging.getLogger("httpx").setLevel(logging.WARNING)
logging.getLogger("telegram").setLevel(logging.WARNING)

def main() -> None:
    """Run the bot."""
    setup_database()
    print("Bot is running")
    application = Application.builder().token('7572707557:AAHRb6tdvbnAQemj6K0EzgMrBaTpVDvTuQQ').build()
    register_handlers(application)
    try:
        application.run_polling(allowed_updates=Update.ALL_TYPES)
    except Exception as e:
        logger.error(f"An error occurred: {e}")

#הרצה
if __name__ == '__main__':
    main()



