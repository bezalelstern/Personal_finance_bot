import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database.models import FixedIncome, TemporaryIncome, FixedExpenses, TemporaryExpenses, Categorise


#חיבור לדאטאבייס
connection_url = "postgresql://admin:1234@localhost:5433/personal_financial_assistant"
engine = create_engine(connection_url)
Session = sessionmaker(bind=engine)
session = Session()

# פונקציה לשליפת נתונים לפי קטגוריה (הוצאות או הכנסות)
def fetch_data_by_category(model):
    """שליפת נתונים לפי קטגוריה (הוצאות או הכנסות)."""
    result = session.query(Categorise.category_name, model.amount) \
                    .select_from(Categorise) \
                    .join(model, model.category_id == Categorise.id) \
                    .all()
    df = pd.DataFrame(result, columns=['category', 'amount'])
    return df

# פונקציה לשליפת כל הנתונים מהדאטאבייס והמרה ל-DataFrame
def fetch_table_data(model, columns):
    results = session.query(*columns).all()
    df = pd.DataFrame(results, columns=[col.name for col in columns])
    if 'time' in df.columns:
        df['time'] = pd.to_datetime(df['time'])
    close_session()
    return df


def csv_data(model):
    # שליפת כל הרשומות
    results = session.query(model).all()

    # המרת התוצאות לרשימת מילונים
    data = [
        {column.name: getattr(record, column.name) for column in model.__table__.columns}
        for record in results
    ]

    # יצירת DataFrame
    df = pd.DataFrame(data)
    return df

# טבלאות לשליפה
tables = {
    "Fixed Incomes": (FixedIncome, [FixedIncome.time, FixedIncome.amount]),
    "Temporary Incomes": (TemporaryIncome, [TemporaryIncome.time, TemporaryIncome.amount]),
    "Fixed Expenses": (FixedExpenses, [FixedExpenses.time, FixedExpenses.amount]),
    "Temporary Expenses": (TemporaryExpenses, [TemporaryExpenses.time, TemporaryExpenses.amount]),
}

def close_session():
    session.close()
