
from telegram import Update
from telegram.ext import CallbackContext
from database.models import TemporaryIncome, TemporaryExpenses, Categorise

from graphs.graph_service.data_from_db import fetch_data_by_category, close_session
from graphs.graph_service.pie_graph_service import send_pie_chart
from telegram_repository.analize_repo import generate_report


# פונקציה לשליחת גרף עוגה להוצאות לפי קטגוריה
async def send_expenses_pie_chart(update: Update, context: CallbackContext) -> None:
    # שליפת נתונים
    df = fetch_data_by_category(TemporaryExpenses)

    # שליחת הגרף

    await send_pie_chart(update, context, df, 'Expenses by categories', 'pie_chart.png')
    await generate_report(update, context)

    close_session()


# פונקציה לשליחת גרף עוגה להכנסות לפי קטגוריה
async def send_incomes_pie_chart(update: Update, context: CallbackContext) -> None:
    # שליפת נתונים
    df = fetch_data_by_category(TemporaryIncome)

    # שליחת הגרף
    await send_pie_chart(update, context, df, 'הכנסות לפי קטגוריה', 'income_pie_chart.png')
    await generate_report(update, context)

    close_session()

