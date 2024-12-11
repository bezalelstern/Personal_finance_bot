
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ContextTypes, ConversationHandler, MessageHandler, CommandHandler, filters

from repository.postgres_repo import save_temporary_expenses_to_db, save_fixed_expenses_to_db
from repository.postgres_repo import create_report, setup_database, save_temporary_expenses_to_db, save_fixed_expenses_to_db, create_category
from telegram_repository.main_repo import start_timer, EXPENSE_TYPE, CATEGORY, AMOUNT, get_keyboard_with_cancel, start, \
    cancel

from texts import help_text, EXPENSE_CATEGORIES, welcome_text, MAIN_KEYBOARD, CATEGORY_MAPPING


async def add_expense_start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data.clear()  # Clear any previous conversation data
    types = [["Fixed Expense", "Temporary Expense"],["❌ Cancel"]]
    await start_timer(context)
    reply_markup = ReplyKeyboardMarkup(types, resize_keyboard=True, one_time_keyboard=True)

    await update.message.reply_text(
        "Please select the type of expense (Fixed or Temporary):",
        reply_markup=reply_markup
    )
    return EXPENSE_TYPE

async def get_expense_type(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    expense_type = update.message.text
    if expense_type == "❌ Cancel":
        return await cancel(update, context)
    context.user_data["expense_type"] = expense_type

    # יצירת מקלדת עם הקטגוריות
    keyboard = EXPENSE_CATEGORIES
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=True)

    await start_timer(context)
    await update.message.reply_text(
        "Please select a category for your expense 📂:",
        reply_markup=reply_markup
    )
    return CATEGORY

async def get_category(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    # טקסט הבחירה שהמשתמש שלח
    selected_text = update.message.text
    print(selected_text)
    if selected_text == "❌ Cancel":
        return await cancel(update, context)
    # המרת הטקסט לשם הקטגוריה
    category = CATEGORY_MAPPING.get(selected_text, 'Unknown')


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
        expense_type = context.user_data['expense_type']

        if expense_type == 'Fixed Expense':
            save_fixed_expenses_to_db(user_id, category, amount)
        elif expense_type == 'Temporary Expense':
            save_temporary_expenses_to_db(user_id, category, amount)

        confirmation = (
            f"✅ Expense Saved!\n"
            f"📂 Category: {category}\n"
            f"💰 Amount: {amount:.2f}"
        )

        reply_markup = ReplyKeyboardMarkup(MAIN_KEYBOARD, resize_keyboard=True)
        await start_timer(context)
        await update.message.reply_text(
            confirmation,
            reply_markup=reply_markup
        )
        return ConversationHandler.END
    except ValueError:
        await start_timer(context)
        await update.message.reply_text("Please enter a valid positive number.")
        return AMOUNT


async def handle_any_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle any user message to reset the timer."""
    await start_timer(context)

# Add a handler for any message
