from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ContextTypes
from analytics.predictions import ExpenseAnalyzer
from analytics.insights import InsightGenerator
from telegram_repository.analize_repo import generate_report



async def send_expense_prediction(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send expense prediction."""
    user_id = update.effective_user.id
    analyzer = ExpenseAnalyzer(user_id)

    next_month_prediction = analyzer.predict_next_month()
    if next_month_prediction is None:
        await update.message.reply_text(
            "📊 We couldn't predict next month's expenses. Please add more data."
        )
        return   await generate_report(update, context)


    patterns = analyzer.identify_spending_patterns()
    if not patterns:
        await update.message.reply_text(
            "📊 No spending patterns identified. Make sure you have provided historical data."
        )
        return   await generate_report(update, context)

    message = (
        f"📊 *Expense Prediction for Next Month:*\n"
        f"Expected Expenses: ₪{next_month_prediction:,.2f}\n\n"
        f"*Spending Patterns:*\n"
        f"• Day with the highest spending: {patterns.get('highest_spending_day', 'Not available')}\n"
        f"• Most expensive category: {patterns.get('highest_spending_category', 'Not available')}\n"
        f"• Average daily spending: ₪{patterns.get('average_daily_spending', 0):,.2f}"
    )

    await update.message.reply_text(message, parse_mode='Markdown')
    await generate_report(update, context)



async def send_savings_insights(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send savings insights."""
    user_id = update.effective_user.id
    insight_gen = InsightGenerator(user_id)

    insights = insight_gen.generate_savings_opportunities()
    if not insights:
        insights = ["💡 No savings opportunities identified."]

    anomalies = insight_gen.get_expense_anomalies()

    message = "*💡 Savings Insights:*\n\n"
    message += "\n".join(insights)

    if anomalies.empty:
        message += "\n\n⚠️ No spending anomalies detected."
    else:
        message += "\n\n*⚠️ Spending Anomalies Detected:*\n"
        for _, row in anomalies.iterrows():
            message += f"• {row['date'].strftime('%d/%m/%Y')}: ₪{row['amount']:,.2f}\n"

    await update.message.reply_text(message, parse_mode='Markdown')
    await generate_report(update, context)
