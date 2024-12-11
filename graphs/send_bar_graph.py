from telegram import Update
from telegram.ext import CallbackContext

from graphs.graph_service.bar_graph_service import create_bar_chart
from graphs.graph_service.data_from_db import fetch_table_data, tables


# יצירת גרפים ושליחתם לבוט
async def generate_charts(update: Update, context: CallbackContext):
    for title, (model, cols) in tables.items():
        df = fetch_table_data(model, cols)
        if not df.empty:
            await create_bar_chart(update, context, df, 'time', 'amount', title, title.replace(" ", "_"))
        else:
            print(f"טבלה ריקה: {title}")


