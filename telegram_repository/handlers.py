from telegram.ext import Application, CommandHandler, MessageHandler, filters, ConversationHandler,ContextTypes
from graphs.send_csv import send_expenses_csv
from graphs.send_histogram_graph import generate_histogram
from graphs.send_line_graph import generate_line_graph
from graphs.send_pie_graph import send_expenses_pie_chart
from telegram_repository.analytics_commands import send_expense_prediction, send_savings_insights
from telegram_repository.csv_service import process_csv
from telegram_repository.income_repo import add_income_start, get_income_type, get_income_amount, save_income
from telegram_repository.expense_repo import add_expense_start, get_category, save_expense, EXPENSE_TYPE,handle_expense_choice
from telegram_repository.analize_repo import display_analyse_menu
from telegram_repository.main_repo import CATEGORY, AMOUNT, cancel, INCOME_TYPE, INCOME_AMOUNT, INCOME_DESCRIPTION, \
    start, help_command, back
from telegram_repository.news_repo import search_news, get_news



def register_handlers(application: Application) -> None:
    """Register all handlers to the application."""
    conv_handler_expense = ConversationHandler(
        entry_points=[MessageHandler(filters.Regex('^💸 Add Expense$'), add_expense_start)],
        states={
            EXPENSE_TYPE: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, handle_expense_choice)
            ],
            CATEGORY: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, get_category)
            ],
            AMOUNT: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, save_expense)
            ],
            4: [
                MessageHandler(filters.Document.ALL, process_csv)
            ],
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
            INCOME_DESCRIPTION: [MessageHandler(filters.TEXT & ~filters.COMMAND, save_income)]
        },
        fallbacks=[
            MessageHandler(filters.Regex('^❌ Cancel$'), cancel),
            CommandHandler('cancel', cancel)
        ]
    )

    conv_handler_news = ConversationHandler(
        entry_points=[MessageHandler(filters.Regex('^Search News$'), search_news)],
        states={
            1: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_news)]
        },
        fallbacks=[CommandHandler('cancel', cancel)]
    )

    # Add conversation handlers
    application.add_handler(conv_handler_expense)
    application.add_handler(conv_handler_income)
    application.add_handler(conv_handler_news)

    # Add simple command handlers
    application.add_handler(CommandHandler('start', start))
    application.add_handler(CommandHandler('help', help_command))
    application.add_handler(CommandHandler('cancel', cancel))

    # Add message handlers
    application.add_handler(MessageHandler(filters.Regex('^❓ Help'), help_command))
    application.add_handler(MessageHandler(filters.Regex('^📊 Report$'), display_analyse_menu))
    application.add_handler(MessageHandler(filters.Regex('^📅 Export csv file$'), send_expenses_csv))
    application.add_handler(MessageHandler(filters.Regex('^📉 Expense pie graph$'), send_expenses_pie_chart))
    application.add_handler(MessageHandler(filters.Regex('^📈 Line graph$'), generate_line_graph))
    application.add_handler(MessageHandler(filters.Regex('^📈 histogram graph$'), generate_histogram))
    application.add_handler(MessageHandler(filters.Regex('^🔙 Back$'), back))
    application.add_handler(MessageHandler(filters.Regex('^📊 Expense Prediction$'), send_expense_prediction))
    application.add_handler(MessageHandler(filters.Regex('^💡 Savings Insights$'), send_savings_insights))


