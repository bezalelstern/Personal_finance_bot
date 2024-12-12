import os
import matplotlib.pyplot as plt
from telegram import Update
from telegram.ext import CallbackContext
import pandas as pd

# פונקציה לשליחת גרף עוגה כללי
async def send_pie_chart(update, context, df: pd.DataFrame, title: str, chart_filename: str) -> None:
    """שליחת גרף עוגה כללי."""

    if not df.empty:
        # קיבוץ לפי קטגוריה וסיכום הסכומים
        df_grouped = df.groupby('category', as_index=False)['amount'].sum()

        # יצירת גרף עוגה
        plt.figure(figsize=(10, 8))
        explode = [0.1] + [0] * (len(df_grouped['category']) - 1)  # הדגשת הפריט הראשון
        colors = ['#ff9999', '#66b3ff', '#99ff99', '#ffcc99', '#c2c2f0', '#ffb3e6']

        wedges, texts, autotexts = plt.pie(
            df_grouped['amount'],
            labels=df_grouped['category'],
            autopct='%1.1f%%',
            startangle=90,
            colors=colors[:len(df_grouped['category'])],
            explode=explode
        )
        plt.title(title, fontsize=16, fontweight='bold')

        # הוספת מקרא אם לא קיים
        plt.legend(wedges, df_grouped['category'], title="category", loc="best", bbox_to_anchor=(0.85, 0.1, 0.5, 1))

        # שמירת התמונה
        plt.savefig(chart_filename, bbox_inches='tight')
        plt.close()

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

