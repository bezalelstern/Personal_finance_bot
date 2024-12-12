import matplotlib.pyplot as plt
import os
from telegram import Update
from telegram.ext import CallbackContext


# פונקציה ליצירת היסטוגרמה
async def create_graph_histogram(update, context, df, x_col, y_col, title, chart_name):
    # יצירת הגרף
    plt.figure(figsize=(12, 8))
    colors = ['orange', 'skyblue', 'lightgreen', 'salmon', 'violet']

    # בניית ההיסטוגרמה עם צבע יחיד
    counts, bins, patches = plt.hist(
        df[x_col].dt.strftime('%Y-%m-%d'),
        bins=5, color=colors[0], edgecolor='black', rwidth=0.8
    )

    # כותרות וצירים
    plt.title(title, fontsize=16, fontweight='bold')
    plt.xlabel(x_col.capitalize(), fontsize=14)
    plt.ylabel("Count", fontsize=14)

    # הוספת מקרא
    for patch, count, bin_left, bin_right in zip(patches, counts, bins[:-1], bins[1:]):
        bin_label = f'{bin_left:.0f} - {bin_right:.0f}'
        plt.text(
            patch.get_x() + patch.get_width() / 2,
            patch.get_height() + 0.5,
            f'{int(count)}',
            ha='center', fontsize=12, color='black'
        )

    plt.grid(axis='y', linestyle='--', alpha=0.7)

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
