import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ConversationHandler, CallbackContext

from data_from_db import generate_charts
from send_bar_graph import create_bar_chart
from telegram_repository.income_repo import add_income_start, get_income_type, get_income_amount, save_income
from repository.db import  setup_database
from telegram_repository.expense_repo import add_expense_start, get_category, save_expense, cancel, start, help_command, \
    CATEGORY, AMOUNT, INCOME_TYPE, INCOME_DESCRIPTION, INCOME_AMOUNT, EXPENSE_TYPE, get_expense_type

from telegram_repository.analize_repo import generate_report

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)
logging.getLogger("httpx").setLevel(logging.WARNING)
logging.getLogger("telegram").setLevel(logging.WARNING)


def main(get_expence_type=None) -> None:
    """Run the bot."""
    setup_database()

    application = Application.builder().token('7349809392:AAHRKfATE1rMImHVejkOeF1Y9afAZz4HE6w').build()

    # Conversation handler for adding expenses
    conv_handler_expense = ConversationHandler(
        entry_points=[MessageHandler(filters.Regex('^💸 Add Expense$'), add_expense_start)],
        states={
            EXPENSE_TYPE: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_expense_type)],
            CATEGORY: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_category)],
            AMOUNT: [MessageHandler(filters.TEXT & ~filters.COMMAND, save_expense)]
        },
        fallbacks=[
            MessageHandler(filters.Regex('^❌ Cancel$'), cancel),
            CommandHandler('cancel', cancel)
        ]
    )

    conv_handler_income = ConversationHandler(
        entry_points=[MessageHandler(filters.Regex('^💰 Add Income$'), add_income_start)],
        states={
            INCOME_TYPE: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_income_type)],
            INCOME_AMOUNT: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_income_amount)],
            INCOME_DESCRIPTION: [MessageHandler(filters.TEXT & ~filters.COMMAND, save_income)]},
        fallbacks=[
            MessageHandler(filters.Regex('^❌ Cancel$'), cancel),
            CommandHandler('cancel', cancel)]
    )

    # Register handlers
    application.add_handler(CommandHandler('start', start))
    application.add_handler(CommandHandler('help', help_command))
    application.add_handler(conv_handler_expense)
    application.add_handler(conv_handler_income)
    application.add_handler(MessageHandler(filters.Regex('^📊 Report$'), generate_report))
    application.add_handler(MessageHandler(filters.Regex('^❓ Help$'), help_command))
    application.add_handler(MessageHandler(filters.Regex('^📅 Daily Report$'), generate_charts))
    application.add_handler(MessageHandler(filters.Regex('^pachshis'), generate_charts))
    # application.add_handler(MessageHandler(filters.Regex('^📉 Monthly Report'),monthly_report))
    # Run the bot
    application.run_polling(allowed_updates=Update.ALL_TYPES)
    print("bot is running")

#הרצה
if __name__ == '__main__':
    main()



