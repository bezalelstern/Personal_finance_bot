import os

from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext
import matplotlib.pyplot as plt
from fake_data import df

# פונקציה ליצירת גרף עוגה
async def send_pie_chart(update: Update, context: CallbackContext) -> None:
    """Send a pie chart for expenses by category."""

    # יצירת גרף עוגה
    plt.figure(figsize=(8, 8))
    plt.pie(df['amount'], labels=df['category'], autopct='%1.1f%%', startangle=90,
            colors=['#ff9999', '#66b3ff', '#99ff99', '#ffcc99'])
    plt.title('Expenses by Category')

    # שמירת התמונה
    plt.savefig('pie_chart.png')

    # שליחת התמונה
    with open('pie_chart.png', 'rb') as photo:
        await update.message.reply_photo(photo=photo)

    # מחיקת התמונה אחרי שליחה
    os.remove('pie_chart.png')
