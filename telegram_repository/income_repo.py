from telegram.ext import ContextTypes, ConversationHandler
from repository.postgres_repo import save_temporary_income_to_db, save_fixed_income_to_db
from telegram import Update, ReplyKeyboardMarkup
from telegram_repository.main_repo import INCOME_TYPE, INCOME_AMOUNT, INCOME_DESCRIPTION, cancel
from texts import MAIN_KEYBOARD


async def add_income_start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Start adding an income."""
    income_types = [["Fixed Income", "Temporary Income"],["❌ Cancel"]]
    reply_markup = ReplyKeyboardMarkup(income_types, resize_keyboard=True, one_time_keyboard=True)

    await update.message.reply_text(
        "Please select a type of income:",
        reply_markup=reply_markup
    )
    return INCOME_TYPE



async def get_income_type(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Store the income type and ask for the amount."""
    context.user_data['income_type'] = update.message.text
    if context.user_data['income_type'] == "❌ Cancel":
        return await cancel(update, context)
    await update.message.reply_text("How much was the income?")
    return INCOME_AMOUNT




async def get_income_amount(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Store the income amount and ask for a description."""
    try:
        amount = float(update.message.text)
        context.user_data['income_amount'] = amount
        await update.message.reply_text("Please provide a description for the income:")
        return INCOME_DESCRIPTION
    except ValueError:
        await update.message.reply_text("Please enter a valid number.")
        return INCOME_AMOUNT



async def save_income(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Save the income to the database."""
    try:
        description = update.message.text
        income_type = context.user_data['income_type']
        amount = context.user_data['income_amount']
        user_id = update.effective_user.id

        if income_type == 'Temporary Income':
            save_temporary_income_to_db(user_id, amount,description)

        elif income_type == 'Fixed Income':
            save_fixed_income_to_db(user_id, amount,description)


        await update.message.reply_text(
            f"✅ Income saved!\n"
            f"Type: {income_type}\n"
            f"Amount: {amount}\n"
            f"Description: {description}",
            reply_markup=ReplyKeyboardMarkup(MAIN_KEYBOARD, resize_keyboard=True)
        )
        return ConversationHandler.END
    except ValueError:
        await update.message.reply_text("There was an error saving your income. Please try again.")
        return INCOME_DESCRIPTION