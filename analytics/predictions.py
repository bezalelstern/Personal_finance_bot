from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler
import pandas as pd
from datetime import datetime, timedelta

from database.config_postgres import db_session
from database.models import TemporaryExpenses, FixedExpenses


class ExpenseAnalyzer:
    def __init__(self, user_id):
        self.user_id = user_id
        self.scaler = StandardScaler()
    
    def get_historical_data(self):
        """אחזור וארגון נתונים היסטוריים"""
        # שליפת כל ההוצאות
        expenses = db_session.query(
            TemporaryExpenses.amount,
            TemporaryExpenses.time,
            TemporaryExpenses.category_id
        ).filter(
            TemporaryExpenses.user_id == self.user_id
        ).all()
        
        df = pd.DataFrame(expenses, columns=['amount', 'date', 'category'])
        df['date'] = pd.to_datetime(df['date'])
        return df.sort_values('date')

    def predict_next_month(self):
        """חיזוי הוצאות לחודש הבא"""
        df = self.get_historical_data()
        
        # עיבוד הנתונים לפורמט מתאים למודל
        df['month'] = df['date'].dt.month
        monthly_expenses = df.groupby('month')['amount'].sum().reset_index()
        
        X = monthly_expenses['month'].values.reshape(-1, 1)
        y = monthly_expenses['amount'].values
        
        model = LinearRegression()
        model.fit(X, y)
        
        next_month = (datetime.now().month % 12) + 1
        prediction = model.predict([[next_month]])
        
        return round(prediction[0], 2)

    def identify_spending_patterns(self):
        """זיהוי דפוסי הוצאות"""
        df = self.get_historical_data()
        patterns = {
            'highest_spending_day': df.groupby(df['date'].dt.day)['amount'].mean().idxmax(),
            'highest_spending_category': df.groupby('category')['amount'].sum().idxmax(),
            'average_daily_spending': df.groupby(df['date'].dt.date)['amount'].sum().mean()
        }
        return patterns 