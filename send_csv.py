import pandas as pd
from telegram import Update
from telegram.ext import CallbackContext
import os

# דוגמת נתונים
from fake_data import df

# פונקציה לשמירת הנתונים כקובץ CSV
async def send_expenses_csv(update: Update, context: CallbackContext) -> None:
    """Send the expense data as a CSV file."""

    # יצירת קובץ CSV
    csv_filename = 'expenses_data.csv'
    df.to_csv(csv_filename, index=False)

    # שליחת הקובץ
    with open(csv_filename, 'rb') as file:
        await update.message.reply_document(document=file)

    # מחיקת הקובץ אחרי שליחה
    os.remove(csv_filename)
