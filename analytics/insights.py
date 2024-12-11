from collections import defaultdict
from database.models import TemporaryExpenses, Categorise


class InsightGenerator:
    def __init__(self, user_id):
        self.user_id = user_id

    def generate_savings_opportunities(self):
        """זיהוי הזדמנויות לחיסכון"""
        expenses = self.get_recent_expenses()
        insights = []
        
        # זיהוי קטגוריות עם הוצאות גבוהות
        if expenses['food'] > 2000:
            insights.append("💡 We identified high spending on food. Consider cooking at home.")
            
        if expenses['entertainment'] > 1000:
            insights.append("💡 You can save on entertainment by looking for deals and discounts.")
            
        return insights

    def get_expense_anomalies(self):
        """זיהוי חריגות בהוצאות"""
        df = self.get_historical_data()
        
        # חישוב ממוצע וסטיית תקן
        mean = df['amount'].mean()
        std = df['amount'].std()
        
        anomalies = df[df['amount'] > mean + 2*std]
        return anomalies 