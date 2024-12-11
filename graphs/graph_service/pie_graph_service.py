import os
import matplotlib.pyplot as plt
from telegram import Update
from telegram.ext import CallbackContext
import pandas as pd

# פונקציה לשליחת גרף עוגה כללי
async def send_pie_chart(update: Update, context: CallbackContext, df: pd.DataFrame, title: str,
                         chart_filename: str) -> None:
    """שליחת גרף עוגה כללי."""

    if not df.empty:
        # יצירת גרף עוגה
        plt.figure(figsize=(8, 8))
        plt.pie(df['amount'], labels=df['category'], autopct='%1.1f%%', startangle=90,
                colors=['#ff9999', '#66b3ff', '#99ff99', '#ffcc99'])
        plt.title(title)

        # שמירת התמונה
        plt.savefig(chart_filename)

        # שליחת התמונה
        try:
            with open(chart_filename, 'rb') as photo:
                await update.message.reply_photo(photo=photo)
            print(f"נשלח גרף עוגה: {chart_filename}")
        except Exception as e:
            print(f"שגיאה בשליחת הגרף: {e}")
        finally:
            # מחיקת התמונה אחרי שליחה
            if os.path.exists(chart_filename):
                os.remove(chart_filename)
    else:
        print(f"לא נמצאו נתונים עבור: {title}")

