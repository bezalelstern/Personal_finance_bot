import logging
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, ConversationHandler
from repository.db import create_report, setup_database, save_expense_to_db, create_category
from texts import help_text, EXPENSE_CATEGORIES, welcome_text, MAIN_KEYBOARD


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

CATEGORY, AMOUNT = range(2)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:

    reply_markup = ReplyKeyboardMarkup(MAIN_KEYBOARD, resize_keyboard=True)

    await update.message.reply_text(
        welcome_text,
        reply_markup=reply_markup
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:

    reply_markup = ReplyKeyboardMarkup(MAIN_KEYBOARD, resize_keyboard=True)

    await update.message.reply_text(help_text, reply_markup=reply_markup)


async def add_expense_start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data.clear()  # Clear any previous conversation data

    keyboard = [category for category in EXPENSE_CATEGORIES]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=True)

    await update.message.reply_text(
        "Please select a category for your expense 📂:",
        reply_markup=reply_markup
    )
    return CATEGORY


async def get_category(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    category = update.message.text.split()[-1]  # Extract category without emoji
    context.user_data['category'] = category

    await update.message.reply_text(
        "How much was the expense? 💰\n"
        "(Enter the amount in your local currency)"
    )
    return AMOUNT


async def save_expense(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Save the expense to the database."""
    try:
        amount = float(update.message.text)
        if amount <= 0:
            raise ValueError("Amount must be positive")

        user_id = update.effective_user.id
        category = context.user_data['category']

        save_expense_to_db(user_id, category, amount)

        # Confirmation message with details
        confirmation = (
            f"✅ Expense Saved!\n"
            f"📂 Category: {category}\n"
            f"💰 Amount: {amount:.2f}"
        )

        reply_markup = ReplyKeyboardMarkup(MAIN_KEYBOARD, resize_keyboard=True)

        await update.message.reply_text(
            confirmation,
            reply_markup=reply_markup
        )
        return ConversationHandler.END
    except ValueError:
        await update.message.reply_text("Please enter a valid positive number.")
        return AMOUNT


async def generate_report(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Generate an expense report."""
    user_id = update.effective_user.id
    results = create_report(user_id)

    reply_markup = ReplyKeyboardMarkup(MAIN_KEYBOARD, resize_keyboard=True)

    if not results:
        await update.message.reply_text(
            "No expenses recorded yet. Start tracking your spending! 💰",
            reply_markup=reply_markup
        )
        return

    report = "📊 Expense Report:\n\n"
    total_expenses = 0
    for category, total, count in results:
        report += f"{category}: {total:.2f} (Transactions: {count})\n"
        total_expenses += total

    report += f"\nTotal Expenses: {total_expenses:.2f}"


    await update.message.reply_text(
        report,
        reply_markup=reply_markup
    )


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Cancel the current conversation."""
    reply_markup = ReplyKeyboardMarkup(MAIN_KEYBOARD, resize_keyboard=True)

    await update.message.reply_text(
        "Operation canceled. What would you like to do next? 🤔",
        reply_markup=reply_markup
    )
    return ConversationHandler.END


def main() -> None:
    """Run the bot."""
    setup_database()

    # Replace with your actual bot token
    application = Application.builder().token('7349809392:AAHRKfATE1rMImHVejkOeF1Y9afAZz4HE6w').build()

    # Conversation handler for adding expenses
    conv_handler = ConversationHandler(
        entry_points=[MessageHandler(filters.Regex('^💸 Add Expense$'), add_expense_start)],
        states={
            CATEGORY: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_category)],
            AMOUNT: [MessageHandler(filters.TEXT & ~filters.COMMAND, save_expense)]
        },
        fallbacks=[
            MessageHandler(filters.Regex('^❌ Cancel$'), cancel),
            CommandHandler('cancel', cancel)
        ]
    )

    # Register handlers
    application.add_handler(CommandHandler('start', start))
    application.add_handler(CommandHandler('help', help_command))
    application.add_handler(conv_handler)
    application.add_handler(MessageHandler(filters.Regex('^📊 Report$'), generate_report))
    application.add_handler(MessageHandler(filters.Regex('^❓ Help$'), help_command))

    # Run the bot
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == '__main__':
    main()


