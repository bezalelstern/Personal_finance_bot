from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import ContextTypes, ConversationHandler
from repository.postgres_repo import  insert_new_expense
from repository.postgres_repo import save_temporary_expenses_to_db, save_fixed_expenses_to_db
from telegram_repository.main_repo import start_timer, EXPENSE_TYPE, CATEGORY, AMOUNT, cancel
from texts import help_text, EXPENSE_CATEGORIES, welcome_text, MAIN_KEYBOARD, CATEGORY_MAPPING


async def add_expense_start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Start the process of adding an expense or uploading a CSV file."""
    context.user_data.clear()
    types = [["Fixed Expense", "Temporary Expense"], ["📂 Upload CSV"], ["❌ Cancel"]]
    await start_timer(context)
    reply_markup = ReplyKeyboardMarkup(types, resize_keyboard=True, one_time_keyboard=True)

    await update.message.reply_text(
        "Please select the type of expense (Fixed or Temporary) or upload a CSV file:",
        reply_markup=reply_markup
    )
    return EXPENSE_TYPE

async def handle_expense_choice(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handle the user's choice for expense type or CSV upload."""
    choice = update.message.text

    if choice == "📂 Upload CSV":
        return await upload_csv(update, context)
    elif choice in ["Fixed Expense", "Temporary Expense"]:
        context.user_data["expense_type"] = choice
        return await get_expense_type(update, context)
    elif choice == "❌ Cancel":
        return await cancel(update, context)
    else:
        await update.message.reply_text("Invalid option. Please try again.")
        return EXPENSE_TYPE

async def get_expense_type(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    expense_type = update.message.text

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


async def upload_csv(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Prompt the user to upload a CSV file."""
    await update.message.reply_text(
        "Please upload a CSV file containing your expenses. 📄",
        reply_markup=ReplyKeyboardRemove()
    )
    return 1

async def process_csv(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Process the uploaded CSV file and save the data."""
    try:
        # Ensure a file is uploaded
        if not update.message.document:
            await update.message.reply_text("No file was uploaded. Please upload a CSV file.")
            return 1

        file = update.message.document
        if file.mime_type != 'text/csv':
            await update.message.reply_text("The file is not a CSV. Please upload a valid CSV file.")
            return 1

        # Download the file to the local system
        file_obj = await context.bot.get_file(file.file_id)
        downloaded_file = await file_obj.download_to_drive()  # הורדה למערכת המקומית

        # Process the file
        insert_new_expense(downloaded_file)
        await update.message.reply_text("✅ All expenses from the CSV were saved successfully!")
        return ConversationHandler.END

    except Exception as e:
        await update.message.reply_text(
            f"An error occurred while processing the file: {str(e)}"
        )
        return 1

