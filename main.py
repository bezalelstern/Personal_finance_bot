import logging
import sqlite3
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, ConversationHandler

# Logging configuration
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# States for conversation handler
CATEGORY, AMOUNT = range(2)

# Database setup
def setup_database():
    conn = sqlite3.connect('expenses.db')
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS expenses (
        id INTEGER PRIMARY KEY,
        user_id INTEGER,
        category TEXT,
        amount REAL,
        date DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    conn.commit()
    conn.close()

def create_report(user_id):
    conn = sqlite3.connect('expenses.db')
    cursor = conn.cursor()

    # Total expenses by category
    cursor.execute('''
            SELECT category, 
                   SUM(amount) as total_amount, 
                   COUNT(*) as transaction_count 
            FROM expenses 
            WHERE user_id = ? 
            GROUP BY category 
            ORDER BY total_amount DESC
        ''', (user_id,))

    results = cursor.fetchall()
    conn.close()
    return results

def save_expense_to_db(user_id, category, amount):
    conn = sqlite3.connect('expenses.db')
    cursor = conn.cursor()
    cursor.execute(
        'INSERT INTO expenses (user_id, category, amount) VALUES (?, ?, ?)',
        (user_id, category, amount)
    )
    conn.commit()
    conn.close()

# Start command handler
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Start the bot and show options."""
    setup_database()

    keyboard = [["💸 Add Expense", "📊 Report"], ["❌ Cancel"]]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

    await update.message.reply_text(
        "Welcome to Expense Tracker Bot! 💰\n\n"
        "Use the buttons below to manage your expenses.",
        reply_markup=reply_markup
    )

# Add expense flow
async def add_expense_start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Start adding an expense."""
    categories = [['Food', 'Transport'], ['Entertainment', 'Shopping'], ['Other']]
    reply_markup = ReplyKeyboardMarkup(categories, resize_keyboard=True, one_time_keyboard=True)

    await update.message.reply_text(
        "Please select a category for your expense:",
        reply_markup=reply_markup
    )
    return CATEGORY

async def get_category(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Store the category and ask for the amount."""
    context.user_data['category'] = update.message.text
    await update.message.reply_text("How much was the expense?")
    return AMOUNT

async def save_expense(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Save the expense to the database."""
    try:
        amount = float(update.message.text)
        category = context.user_data['category']
        user_id = update.effective_user.id

        save_expense_to_db(user_id, category, amount)

        await update.message.reply_text(
            f"✅ Expense saved!\n"
            f"Category: {category}\n"
            f"Amount: {amount}",
            reply_markup=ReplyKeyboardMarkup([["💸 Add Expense", "📊 Report"], ["❌ Cancel"]], resize_keyboard=True)
        )
        return ConversationHandler.END
    except ValueError:
        await update.message.reply_text("Please enter a valid number.")
        return AMOUNT

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Cancel the conversation."""
    await update.message.reply_text(
        "Expense tracking canceled.",
        reply_markup=ReplyKeyboardMarkup([["💸 Add Expense", "📊 Report"], ["❌ Cancel"]], resize_keyboard=True)
    )
    return ConversationHandler.END

# Generate expense report
async def generate_report(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Generate an expense report."""
    user_id = update.effective_user.id
    results = create_report(user_id)

    if not results:
        await update.message.reply_text(
            "No expenses recorded yet.",
            reply_markup=ReplyKeyboardMarkup([["💸 Add Expense", "📊 Report"], ["❌ Cancel"]], resize_keyboard=True)
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
        reply_markup=ReplyKeyboardMarkup([["💸 Add Expense", "📊 Report"], ["❌ Cancel"]], resize_keyboard=True)
    )

# Main function
def main() -> None:
    """Run the bot."""
    setup_database()
    application = Application.builder().token('7349809392:AAHRKfATE1rMImHVejkOeF1Y9afAZz4HE6w').build()

    # Conversation handler for adding expenses
    conv_handler = ConversationHandler(
        entry_points=[MessageHandler(filters.Regex('^💸 Add Expense$'), add_expense_start)],
        states={
            CATEGORY: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_category)],
            AMOUNT: [MessageHandler(filters.TEXT & ~filters.COMMAND, save_expense)]
        },
        fallbacks=[MessageHandler(filters.Regex('^❌ Cancel$'), cancel)]
    )

    # Register handlers
    application.add_handler(CommandHandler('start', start))
    application.add_handler(conv_handler)
    application.add_handler(MessageHandler(filters.Regex('^📊 Report$'), generate_report))

    # Run the bot
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()


