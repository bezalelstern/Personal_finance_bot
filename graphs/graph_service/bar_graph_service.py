import matplotlib.pyplot as plt
import os
from telegram import Update
from telegram.ext import CallbackContext


# פונקציה ליצירת גרף בר ושליחתו לבוט
async def create_bar_chart(update, context, df, x_col, y_col, title, chart_name):
    """יצירת גרף בר ושליחתו לבוט טלגרם."""

    # יצירת הגרף
    plt.figure(figsize=(12, 8))
    colors = ['#ff9999', '#66b3ff', '#99ff99', '#ffcc99', '#c2c2f0', '#ffb3e6']
    bars = plt.bar(df[x_col].dt.strftime('%Y-%m-%d'), df[y_col], color=colors[:len(df)])

    plt.title(title, fontsize=16, fontweight='bold')
    plt.xlabel(x_col.capitalize(), fontsize=12)
    plt.ylabel(y_col.capitalize(), fontsize=12)

    # הוספת מקרא אם לא קיים
    plt.legend(bars, df[x_col].dt.strftime('%Y-%m-%d'), title="Dates", loc="best", bbox_to_anchor=(1.05, 1))

    # שמירת הגרף
    chart_path = f'{chart_name}.png'
    plt.savefig(chart_path, bbox_inches='tight')
    plt.close()

    # שליחת הגרף לבוט
    try:
        with open(chart_path, 'rb') as photo:
            await update.message.reply_photo(photo=photo)
        print(f"נשלח גרף: {chart_path}")
    except Exception as e:
        print(f"שגיאה בשליחת הגרף: {e}")
    finally:
        # מחיקת הגרף לאחר השליחה
        if os.path.exists(chart_path):
            os.remove(chart_path)