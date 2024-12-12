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
            if expenses.get('food', 0) > 2000:
                insights.append("💡 We identified high spending on food. Consider cooking at home.")
            if expenses.get('transport', 0) > 1000:
                insights.append("💡 You can save on transport by using public transportation or carpooling.")
            if expenses.get('rent/utilities', 0) > 1500:
                insights.append("💡 High rent/utilities expenses. Consider reviewing your plans or moving.")
            if expenses.get('groceries', 0) > 1000:
                insights.append("💡 You can save on groceries by meal planning and buying in bulk.")
            if expenses.get('shopping', 0) > 500:
                insights.append("💡 You may want to reduce shopping expenses. Consider budgeting for it.")
            if expenses.get('entertainment', 0) > 1000:
                insights.append("💡 You can save on entertainment by looking for deals and discounts.")
            if expenses.get('health', 0) > 500:
                insights.append("💡 Health expenses are high. Explore ways to save on medications or insurance.")
            if expenses.get('education', 0) > 500:
                insights.append("💡 Consider optimizing education costs by looking for cheaper alternatives.")
            if expenses.get('public transit', 0) > 200:
                insights.append("💡 Public transit expenses could be reduced with monthly passes or discounts.")
            if expenses.get('gifts', 0) > 300:
                insights.append("💡 You can reduce spending on gifts by planning ahead for special occasions.")
            if expenses.get('technology', 0) > 1000:
                insights.append("💡 Technology expenses are high. Consider upgrading only when neces sary.")
            if expenses.get('dining out', 0) > 1500:
                insights.append("💡 Consider cooking more at home to reduce dining out expenses.")
            if expenses.get('fitness', 0) > 300:
                insights.append("💡 Fitness expenses are high. Explore cheaper alternatives like home workouts.")
            if expenses.get('travel', 0) > 2000:
                insights.append("💡 High travel expenses. Look for discounts or cheaper destinations.")
            if expenses.get('other', 0) > 500:
                insights.append("💡 Review your 'other' expenses to identify potential savings opportunities.")

            return insights
        except Exception as e:
            print(f"Error generating savings opportunities: {e}")
            return []

    def get_expense_anomalies(self):
        try:
            df = self.expense_analyzer.get_historical_data()
            mean = df['amount'].mean()
            std = df['amount'].std()
            anomalies = df[df['amount'] > mean + 2*std]
            return anomalies
        except Exception as e:
            print(f"Error identifying expense anomalies: {e}")
            return pd.DataFrame()