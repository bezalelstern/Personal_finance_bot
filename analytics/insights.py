from collections import defaultdict
from datetime import datetime, timedelta
import pandas as pd
from database.config_postgres import db_session
from database.models import TemporaryExpenses, Categorise
from analytics.predictions import ExpenseAnalyzer


class InsightGenerator:
    def __init__(self, user_id):
        self.user_id = user_id
        self.expense_analyzer = ExpenseAnalyzer(user_id)

    def get_recent_expenses(self):
        """שליפת הוצאות אחרונות"""
        try:
            expenses = db_session.query(
                TemporaryExpenses.amount,
                TemporaryExpenses.category_id,
                Categorise.category_name
            ).join(
                Categorise,
                TemporaryExpenses.category_id == Categorise.id
            ).filter(
                TemporaryExpenses.user_id == self.user_id,
                TemporaryExpenses.time >= datetime.now() - timedelta(days=30)
            ).all()

            # המרת תוצאות לדיקט
            expense_dict = {}
            for amount, category_id, category_name in expenses:
                expense_dict[category_name.lower()] = expense_dict.get(category_name.lower(), 0) + amount

            return expense_dict
        except Exception as e:
            print(f"Error retrieving recent expenses: {e}")
            return {}

    def generate_savings_opportunities(self):
        """זיהוי הזדמנויות לחיסכון"""
        try:
            expenses = self.get_recent_expenses()
            insights = []
            # זיהוי קטגוריות עם הוצאות גבוהות
            if expenses['food'] > 2000:
                insights.append("💡 We identified high spending on food. Consider cooking at home.")
            if expenses['entertainment'] > 1000:
                insights.append("💡 You can save on entertainment by looking for deals and discounts.")
            return insights
        except Exception as e:
            print(f"Error generating savings opportunities: {e}")
            return []

    def get_expense_anomalies(self):
        """זיהוי חריגות בהוצאות"""
        try:
            df = self.expense_analyzer.get_historical_data()
            # חישוב ממוצע וסטיית תקן
            mean = df['amount'].mean()
            std = df['amount'].std()
            anomalies = df[df['amount'] > mean + 2*std]
            return anomalies
        except Exception as e:
            print(f"Error identifying expense anomalies: {e}")
            return pd.DataFrame()