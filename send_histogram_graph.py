from telegram import Update
from telegram.ext import CallbackContext
import os
import matplotlib.pyplot as plt


# דוגמת נתונים
from fake_data import df
# פונקציה ליצירת היסטוגרמה
async def send_histogram(update: Update, context: CallbackContext) -> None:
    """Send a histogram of expense amounts."""

    # יצירת היסטוגרמה
    plt.figure(figsize=(10, 6))
    plt.hist(df['amount'], bins=5, color='skyblue', edgecolor='black')
    plt.title('Distribution of Expense Amounts')
    plt.xlabel('Amount')
    plt.ylabel('Frequency')

    # שמירת התמונה
    plt.savefig('histogram.png')

    # שליחת התמונה
    with open('histogram.png', 'rb') as photo:
        await update.message.reply_photo(photo=photo)

    # מחיקת התמונה אחרי שליחה
    os.remove('histogram.png')
