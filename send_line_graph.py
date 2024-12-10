import os

from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext
import matplotlib.pyplot as plt
from fake_data import df


# פונקציה ליצירת גרף קווים
async def send_line_chart(update: Update, context: CallbackContext) -> None:
    """Send a line chart of expenses over time."""

    # יצירת גרף קווים
    plt.figure(figsize=(10, 6))
    plt.plot(df['date'], df['amount'], marker='o', color='b', linestyle='-', linewidth=2, markersize=6)
    plt.title('Expenses Over Time')
    plt.xlabel('Date')
    plt.ylabel('Amount')
    plt.grid(True)

    # שמירת התמונה
    plt.savefig('line_chart.png')

    # שליחת התמונה
    with open('line_chart.png', 'rb') as photo:
        await update.message.reply_photo(photo=photo)

    # מחיקת התמונה אחרי שליחה
    os.remove('line_chart.png')