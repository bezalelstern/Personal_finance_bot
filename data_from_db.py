import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database.models import FixedIncome, TemporaryIncome, FixedExpenses, TemporaryExpenses, Categorise
from send_bar_graph import create_bar_chart
from telegram import Update
from telegram.ext import CallbackContext

connection_url = "postgresql://admin:1234@localhost:5433/personal_financial_assistant"
engine = create_engine(connection_url)
Session = sessionmaker(bind=engine)
session = Session()

# פונקציה לשליפת נתונים ממודל והמרה ל-DataFrame
def fetch_table_data(model, columns):
    results = session.query(*columns).all()
    df = pd.DataFrame(results, columns=[col.name for col in columns])
    if 'time' in df.columns:
        df['time'] = pd.to_datetime(df['time'])
    return df


# טבלאות לשליפה
tables = {
    "Fixed Incomes": (FixedIncome, [FixedIncome.time, FixedIncome.amount]),
    "Temporary Incomes": (TemporaryIncome, [TemporaryIncome.time, TemporaryIncome.amount]),
    "Fixed Expenses": (FixedExpenses, [FixedExpenses.time, FixedExpenses.amount]),
    "Temporary Expenses": (TemporaryExpenses, [TemporaryExpenses.time, TemporaryExpenses.amount]),
}

# יצירת גרפים ושליחתם לבוט
async def generate_charts(update: Update, context: CallbackContext):
    for title, (model, cols) in tables.items():
        df = fetch_table_data(model, cols)
        if not df.empty:
            await create_bar_chart(update, context, df, 'time', 'amount', title, title.replace(" ", "_"))
        else:
            print(f"טבלה ריקה: {title}")
