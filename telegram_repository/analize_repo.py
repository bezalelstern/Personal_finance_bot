from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import CallbackContext


async def generate_report(update: Update, context: CallbackContext) -> None:
    """Display a menu with 5 buttons for report options."""
    
    reply_keyboard = [
        ['📉 Expense pie graph', '📈 Line graph'],
        ['📈 histogram graph', '📅 Export csv file'],
        ["📊 Expense Prediction","💡 Savings Insights"],
        ['🔙 Back']
    ]
    markup = ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True,one_time_keyboard=True)

    await update.message.reply_text(
        "Please choose a report type:",
        reply_markup=markup
    )
