from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ContextTypes
from analytics.predictions import ExpenseAnalyzer
from analytics.insights import InsightGenerator
import matplotlib.pyplot as plt

async def send_expense_prediction(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """שליחת תחזית הוצאות"""
    user_id = update.effective_user.id
    analyzer = ExpenseAnalyzer(user_id)
    
    next_month_prediction = analyzer.predict_next_month()
    patterns = analyzer.identify_spending_patterns()

    message = (
        f"📊 *Expense Prediction for Next Month:*\n"
        f"Expected Expenses: ₪{next_month_prediction:,.2f}\n\n"
        f"*Spending Patterns:*\n"
        f"• Highest Spending Day: {patterns['highest_spending_day']}\n"
        f"• Most Expensive Category: {patterns['highest_spending_category']}\n"
        f"• Daily Average: ₪{patterns['average_daily_spending']:,.2f}"
    )
    
    await update.message.reply_text(message, parse_mode='Markdown')

async def send_savings_insights(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """שליחת תובנות לחיסכון"""
    user_id = update.effective_user.id
    insight_gen = InsightGenerator(user_id)
    
    insights = insight_gen.generate_savings_opportunities()
    anomalies = insight_gen.get_expense_anomalies()

    message = "*💡 Savings Insights:*\n\n"
    message += "\n".join(insights)
    
    if not anomalies.empty:
        message += "\n\n*⚠️ Detected Anomalous Expenses:*\n"
        for _, row in anomalies.iterrows():
            message += f"• {row['date'].strftime('%d/%m/%Y')}: ₪{row['amount']:,.2f}\n"
    
    await update.message.reply_text(message, parse_mode='Markdown') 