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
        try:
            expenses = db_session.query(
                TemporaryExpenses.amount,
                TemporaryExpenses.time,
                TemporaryExpenses.category_id
            ).filter(
                TemporaryExpenses.user_id == self.user_id
            ).all()
            if not expenses:
                raise ValueError("No expense data found for this user")
            df = pd.DataFrame(expenses, columns=['amount', 'date', 'category'])
            df['date'] = pd.to_datetime(df['date'])
            return df.sort_values('date')
        except Exception as e:
            print(f"Error retrieving historical data: {e}")
            return pd.DataFrame()

    def predict_next_month(self):
        """חיזוי הוצאות לחודש הבא"""
        try:
            df = self.get_historical_data()
            # עיבוד הנתונים לפורמט מתאים למודל
            df['month'] = df['date'].dt.month
            monthly_expenses = df.groupby('month')['amount'].sum().reset_index()
            if len(monthly_expenses) < 2:
                print("Not enough historical data for prediction")
                return None
            X = monthly_expenses['month'].values.reshape(-1, 1)
            y = monthly_expenses['amount'].values
            model = LinearRegression()
            model.fit(X, y)
            next_month = (datetime.now().month % 12) + 1
            prediction = model.predict([[next_month]])
            return round(prediction[0], 2)
        except Exception as e:
            print(f"Error in prediction: {e}")
            return None

    def identify_spending_patterns(self):
        """זיהוי דפוסי הוצאות"""
        try:
            df = self.get_historical_data()
            if df.empty:
                return {}
            patterns = {
                'highest_spending_day': df.groupby(df['date'].dt.day)['amount'].mean().idxmax(),
                'highest_spending_category': df.groupby('category')['amount'].sum().idxmax(),
                'average_daily_spending': df.groupby(df['date'].dt.date)['amount'].sum().mean()
            }
            return patterns
        except Exception as e:
            print(f"Error identifying spending patterns: {e}")
            return {}