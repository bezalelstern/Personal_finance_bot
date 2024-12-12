from telegram import Update
from telegram.ext import CallbackContext

from graphs.graph_service.bar_graph_service import create_bar_chart
from graphs.graph_service.data_from_db import fetch_table_data, tables
from telegram_repository.analize_repo import generate_report


# יצירת גרפים ושליחתם לבוט
async def generate_bar_graph(update: Update, context: CallbackContext):
    for title, (model, cols) in tables.items():
        df = fetch_table_data(model, cols)
        if not df.empty:
            await create_bar_chart(update, context, df, 'time', 'amount', title, title.replace(" ", "_"))
            await generate_report(update, context)
        else:
            print(f"טבלה ריקה: {title}")


