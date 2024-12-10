import os

from telegram import Update
from telegram.ext import CallbackContext
import matplotlib.pyplot as plt
from fake_data import df


# פונקציה ליצירת גרף בר
async def send_bar_chart(update: Update, context: CallbackContext) -> None:
    """Send a bar chart for expenses by date."""

    # יצירת גרף בר
    plt.figure(figsize=(10, 6))
    plt.bar(df['date'].dt.strftime('%Y-%m-%d'), df['amount'], color='orange')
    plt.title('Expenses by Date')
    plt.xlabel('Date')
    plt.ylabel('Amount')

    # שמירת התמונה
    plt.savefig('bar_chart.png')

    # שליחת התמונה
    with open('bar_chart.png', 'rb') as photo:
        await update.message.reply_photo(photo=photo)

    # מחיקת התמונה אחרי שליחה
    os.remove('bar_chart.png')
