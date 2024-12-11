from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler
from repository.mongo_repo import get_news_from_last_week

async def search_news(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text("Please enter a keyword to search for news:")
    return 1

async def get_news(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        keyword = update.message.text
        results = get_news_from_last_week(keyword)
        if not results:
            await update.message.reply_text("לא נמצאו כתבות מהשבוע האחרון.")
            return
        for article in results:
            message = f"ערוץ: {article['channel']}\n" \
                      f"הודעה: {article['message']}\n" \
                      f"תאריך: {article['date']}"

            await update.message.reply_text(message)

    except Exception as e:
        await update.message.reply_text(f"אירעה שגיאה: {str(e)}")

    finally:
        return ConversationHandler.END

