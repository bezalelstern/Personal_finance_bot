import os

from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext
import matplotlib.pyplot as plt
from fake_data import df



# פונקציה לשליחת התמונה
async def send_expense_graph(update: Update, context: CallbackContext) -> None:
    """Send the expense graph image."""
    # יצירת הגרף
    plt.figure(figsize=(10, 6))
    plt.bar(df['category'], df['amount'], color='skyblue')
    plt.title('Expenses by Category')
    plt.xlabel('Category')
    plt.ylabel('Amount')
    plt.savefig('expenses_graph.png')

    # שליחת התמונה
    with open('expenses_graph.png', 'rb') as photo:
        await update.message.reply_photo(photo=photo)

    # מחיקת התמונה לאחר שליחה
    os.remove('expenses_graph.png')
