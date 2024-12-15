from telegram import ReplyKeyboardRemove, Update
from telegram.ext import ContextTypes, ConversationHandler

from repository.postgres_repo import insert_new_expense
from telegram_repository.main_repo import back


async def upload_csv(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Prompt the user to upload a CSV file."""
    await update.message.reply_text(
        "Please upload a CSV file containing your expenses. 📄",
        reply_markup=ReplyKeyboardRemove()
    )
    return 4


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
        id = update.effective_user.id
        insert_new_expense(downloaded_file,id)
        await update.message.reply_text("✅ All expenses from the CSV were saved successfully!")
        await back(update, context)
        return ConversationHandler.END

    except Exception as e:
        await update.message.reply_text(
            f"An error occurred while processing the file: {str(e)}"
        )
        return 1