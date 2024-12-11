import logging
from telegram._update import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ConversationHandler,ContextTypes
from graphs.send_bar_graph import generate_bar_graph
from graphs.send_histogram_graph import generate_histogram
from graphs.send_line_graph import generate_line_graph
from graphs.send_pie_graph import send_expenses_pie_chart
from repository.postgres_repo import setup_database
from telegram_repository.income_repo import add_income_start, get_income_type, get_income_amount, save_income
from telegram_repository.expense_repo import add_expense_start, get_category, save_expense, EXPENSE_TYPE, get_expense_type, handle_any_message
from telegram_repository.analize_repo import generate_report
from telegram_repository.main_repo import CATEGORY, AMOUNT, cancel, INCOME_TYPE, INCOME_AMOUNT, INCOME_DESCRIPTION, \
    start, help_command
from telegram_repository.news_repo import search_news, get_news

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)
logging.getLogger("httpx").setLevel(logging.WARNING)
logging.getLogger("telegram").setLevel(logging.WARNING)


def main(get_expence_type=None) -> None:
    """Run the bot."""
    setup_database()
    print("bot is running")
    application = Application.builder().token('7349809392:AAHRKfATE1rMImHVejkOeF1Y9afAZz4HE6w').build()



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
    conv_handler_news = ConversationHandler(
        entry_points=[MessageHandler(filters.Regex('^Search News$'), search_news)],
        states={
            1: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_news)]
        },
        fallbacks=[CommandHandler('cancel', cancel)]
    )
    # Register handlers
    application.add_handler(conv_handler_news)
    application.add_handler(conv_handler_expense)
    application.add_handler(conv_handler_income)
    application.add_handler(CommandHandler('start', start))
    application.add_handler(CommandHandler('help', help_command))
    application.add_handler(MessageHandler(filters.Regex('^📊 Report$'), generate_report))
    application.add_handler(MessageHandler(filters.Regex('^❓ Help$'), help_command))
    application.add_handler(MessageHandler(filters.Regex('^📅 Daily Report$'), generate_bar_graph))
    application.add_handler(MessageHandler(filters.Regex('^📉 Monthly Report$'), send_expenses_pie_chart))
    application.add_handler(MessageHandler(filters.Regex('^📈 Weekly Report$'), generate_line_graph))
    application.add_handler(MessageHandler(filters.Regex('^📊 Yearly Report$'), generate_histogram))
    application.add_handler(MessageHandler(filters.Regex('^🔙 Back$'), start))
    application.run_polling(allowed_updates=Update.ALL_TYPES)


#הרצה
if __name__ == '__main__':
    main()



