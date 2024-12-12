import asyncio
from telegram import ReplyKeyboardMarkup, Update
from telegram.ext import ContextTypes, ConversationHandler
from texts import MAIN_KEYBOARD, help_text, welcome_text

EXPENSE_TYPE, CATEGORY, AMOUNT, INCOME_TYPE, INCOME_AMOUNT, INCOME_DESCRIPTION = range(6)
timer_task = None

def reset_timer(context):
    """Cancel any existing timer task."""
    global timer_task
    if timer_task is not None:
        timer_task.cancel()
        timer_task = None

async def start_timer(context: ContextTypes.DEFAULT_TYPE):
    reset_timer(context)
    try:
        loop = asyncio.get_running_loop()
        global timer_task
        timer_task = loop.create_task(show_start_button(context))
    except RuntimeError:
        timer_task = asyncio.create_task(show_start_button(context))

async def show_start_button(context: ContextTypes.DEFAULT_TYPE):
    try:
        await asyncio.sleep(40)
        keyboard = [["/start"]]
        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

        chat_id = context.user_data.get('chat_id')
        if chat_id:
            await context.bot.send_message(
                chat_id=chat_id,
                text="Start over by clicking the button below:",
                reply_markup=reply_markup
            )
    except asyncio.CancelledError:
        pass

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    context.user_data.clear()
    context.user_data['chat_id'] = update.effective_chat.id
    reply_markup = ReplyKeyboardMarkup(MAIN_KEYBOARD, resize_keyboard=True)
    await start_timer(context)
    await update.message.reply_text(
        welcome_text,
        reply_markup=reply_markup
    )

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Cancel the current conversation."""
    context.user_data.clear()
    context.user_data['chat_id'] = update.effective_chat.id
    reply_markup = ReplyKeyboardMarkup(MAIN_KEYBOARD, resize_keyboard=True)
    await update.message.reply_text(
        "Operation canceled. What would you like to do next? 🤔",
        reply_markup=reply_markup
    )
    return ConversationHandler.END


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    reply_markup = ReplyKeyboardMarkup(MAIN_KEYBOARD, resize_keyboard=True)
    await start_timer(context)
    await update.message.reply_text(help_text, reply_markup=reply_markup)


def get_keyboard_with_cancel(options):
    options_with_cancel = options + [["❌ Cancel"]]
    return ReplyKeyboardMarkup(options_with_cancel, resize_keyboard=True, one_time_keyboard=True)