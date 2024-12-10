from sqlalchemy.orm.sync import update
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ContextTypes, ConversationHandler
from repository.db import create_report, setup_database, save_temporary_expenses_to_db, save_fixed_expenses_to_db, create_category
from texts import help_text, EXPENSE_CATEGORIES, welcome_text, MAIN_KEYBOARD
from telegram.ext import CallbackContext

EXPENSE_TYPE, CATEGORY, AMOUNT, INCOME_TYPE, INCOME_AMOUNT, INCOME_DESCRIPTION = range(6)
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:

    reply_markup = ReplyKeyboardMarkup(MAIN_KEYBOARD, resize_keyboard=True)

    await update.message.reply_text(
        welcome_text,
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

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:

    reply_markup = ReplyKeyboardMarkup(MAIN_KEYBOARD, resize_keyboard=True)

    await update.message.reply_text(help_text, reply_markup=reply_markup)



async def add_expense_start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data.clear()  # Clear any previous conversation data
    types = [['Fixed Expense', 'Temporary Expense']]

    reply_markup = ReplyKeyboardMarkup(types, resize_keyboard=True, one_time_keyboard=True)

    await update.message.reply_text(
        "Please select the type of expense (Fixed or Temporary):",
                                    reply_markup=reply_markup)
    return EXPENSE_TYPE


async def get_expense_type(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    type = update.message.text
    context.user_data["expense_type"] = type
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
        type = context.user_data['expense_type']

        if type == 'Fixed Expense':
            save_fixed_expenses_to_db(user_id, category, amount)

        elif type == 'Temporary Expense':
            save_temporary_expenses_to_db(user_id, category, amount)


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





