import matplotlib.pyplot as plt
import os
from telegram import Update
from telegram.ext import CallbackContext


# פונקציה ליצירת גרף קווים
async def create_line_chart(update: Update, context: CallbackContext, df, x_col, y_col, title, chart_name):
    plt.figure(figsize=(10, 6))
    plt.plote(df[x_col].dt.strftime('%Y-%m-%d'), df[y_col], color='orange')
    plt.title(title)
    plt.xlabel(x_col.capitalize())
    plt.ylabel(y_col.capitalize())

    # שמירת הגרף
    chart_path = f'{chart_name}.png'
    plt.savefig(chart_path)
    plt.close()

    # שליחת הגרף לבוט
    try:
        with open(chart_path, 'rb') as photo:
            await update.message.reply_photo(photo=photo)
        print(f"נשלח גרף: {chart_path}")
    except Exception as e:
        print(f"שגיאה בשליחת הגרף: {e}")

    # מחיקת הגרף לאחר השליחה
    if os.path.exists(chart_path):
        os.remove(chart_path)