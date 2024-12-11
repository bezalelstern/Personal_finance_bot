import logging
import threading

from telegram._update import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ConversationHandler,ContextTypes
from graphs.send_bar_graph import generate_bar_graph
from graphs.send_histogram_graph import generate_histogram
from graphs.send_pie_graph import send_expenses_pie_chart, send_incomes_pie_chart
from repository.mongo_repo import get_news_from_last_week
from repository.postgres_repo import setup_database
from telegram_repository.income_repo import add_income_start, get_income_type, get_income_amount, save_income
from telegram_repository.expense_repo import add_expense_start, get_category, save_expense, cancel, start, help_command, \
    CATEGORY, AMOUNT, INCOME_TYPE, INCOME_DESCRIPTION, INCOME_AMOUNT, EXPENSE_TYPE, get_expense_type



from telegram_repository.analize_repo import generate_report

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)
logging.getLogger("httpx").setLevel(logging.WARNING)
logging.getLogger("telegram").setLevel(logging.WARNING)

async def search_news(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text("Please enter a keyword to search for news:")
    return 1

async def get_news(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        keyword = update.message.text
        results = get_news_from_last_week(keyword)
        if not results:
            await update.message.reply_text("לא נמצאו כתבות מהשבוע האחרון.")
            return
        for article in results:
            message = f"ערוץ: {article['channel']}\n" \
                      f"הודעה: {article['message']}\n" \
                      f"תאריך: {article['date']}"

            await update.message.reply_text(message)

    except Exception as e:
        await update.message.reply_text(f"אירעה שגיאה: {str(e)}")

    finally:
        return ConversationHandler.END


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
    conv_handler_news = ConversationHandler(
        entry_points=[MessageHandler(filters.Regex('^Search News$'), search_news)],
        states={
            1: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_news)]
        },
        fallbacks=[CommandHandler('cancel', cancel)]
    )
    # Register handlers
    application.add_handler(CommandHandler('start', start))
    application.add_handler(CommandHandler('help', help_command))
    application.add_handler(conv_handler_news)
    application.add_handler(conv_handler_expense)
    application.add_handler(conv_handler_income)
    application.add_handler(MessageHandler(filters.Regex('^📊 Report$'), generate_report))
    application.add_handler(MessageHandler(filters.Regex('^❓ Help$'), help_command))
    application.add_handler(MessageHandler(filters.Regex('^📅 Daily Report$'), generate_bar_graph))
    application.add_handler(MessageHandler(filters.Regex('^📉 Monthly Report$'), send_expenses_pie_chart))
    application.add_handler(MessageHandler(filters.Regex('^📈 Weekly Report$'), send_incomes_pie_chart))
    application.add_handler(MessageHandler(filters.Regex('^📊 Yearly Report$'), generate_histogram))

    application.run_polling(allowed_updates=Update.ALL_TYPES)
    print("bot is running")

#הרצה
if __name__ == '__main__':
    main()



