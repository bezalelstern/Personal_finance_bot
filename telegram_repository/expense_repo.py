# import asyncio
# import threading
# from sqlalchemy.orm.sync import update
# from telegram import Update, ReplyKeyboardMarkup
# from telegram.ext import ContextTypes, ConversationHandler
# from repository.db import create_report, setup_database, save_temporary_expenses_to_db, save_fixed_expenses_to_db, create_category
# from texts import help_text, EXPENSE_CATEGORIES, welcome_text, MAIN_KEYBOARD
# EXPENSE_TYPE, CATEGORY, AMOUNT, INCOME_TYPE, INCOME_AMOUNT, INCOME_DESCRIPTION = range(6)
# timer_task = None
#
#
# async def start_timer(context: ContextTypes.DEFAULT_TYPE):
#     """Start the idle timer."""
#     global timer_task
#     if timer_task is not None:
#         timer_task.cancel()
#
#     loop = asyncio.get_running_loop()
#     timer_task = loop.create_task(show_start_button(context))
#
# async def show_start_button(context: ContextTypes.DEFAULT_TYPE):
#     try:
#         await asyncio.sleep(10)  # זמן המתנה של 10 שניות (ניתן לשינוי)
#         keyboard = [["/start"]]
#         reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
#
#         await context.bot.send_message(
#             chat_id=context.job.chat_id,  # שימוש ב-context.job.chat_id במקום
#             text="Start over by clicking the button below:",
#             reply_markup=reply_markup
#         )
#     except asyncio.CancelledError:
#         # אם הטיימר מבוטל, דלג על המשך הביצוע
#         pass
#
# async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
#
#     reply_markup = ReplyKeyboardMarkup(MAIN_KEYBOARD, resize_keyboard=True)
#     await start_timer(context)
#     await update.message.reply_text(
#         welcome_text,
#         reply_markup=reply_markup
#     )
#
# async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
#     """Cancel the current conversation."""
#     reply_markup = ReplyKeyboardMarkup(MAIN_KEYBOARD, resize_keyboard=True)
#     await start_timer(context)
#     await update.message.reply_text(
#         "Operation canceled. What would you like to do next? 🤔",
#         reply_markup=reply_markup
#     )
#     return ConversationHandler.END
#
# async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
#
#     reply_markup = ReplyKeyboardMarkup(MAIN_KEYBOARD, resize_keyboard=True)
#     await start_timer(context)
#     await update.message.reply_text(help_text, reply_markup=reply_markup)
#
#
#
# async def add_expense_start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
#     context.user_data.clear()  # Clear any previous conversation data
#     types = [['Fixed Expense', 'Temporary Expense']]
#     await start_timer(context)
#     reply_markup = ReplyKeyboardMarkup(types, resize_keyboard=True, one_time_keyboard=True)
#
#     await update.message.reply_text(
#         "Please select the type of expense (Fixed or Temporary):",
#                                     reply_markup=reply_markup)
#     return EXPENSE_TYPE
#
#
# async def get_expense_type(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
#     type = update.message.text
#     context.user_data["expense_type"] = type
#     keyboard = [category for category in EXPENSE_CATEGORIES]
#     reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=True)
#     await start_timer(context)
#     await update.message.reply_text(
#         "Please select a category for your expense 📂:",
#         reply_markup=reply_markup
#     )
#     return CATEGORY
#
# async def get_category(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
#     category = update.message.text.split()[-1]  # Extract category without emoji
#     context.user_data['category'] = category
#     await start_timer(context)
#     await update.message.reply_text(
#         "How much was the expense? 💰\n"
#         "(Enter the amount in your local currency)"
#     )
#     return AMOUNT
#
#
#
# async def save_expense(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
#     """Save the expense to the database."""
#     try:
#         amount = float(update.message.text)
#         if amount <= 0:
#             raise ValueError("Amount must be positive")
#
#         user_id = update.effective_user.id
#         category = context.user_data['category']
#         type = context.user_data['expense_type']
#
#         if type == 'Fixed Expense':
#             save_fixed_expenses_to_db(user_id, category, amount)
#
#         elif type == 'Temporary Expense':
#             save_temporary_expenses_to_db(user_id, category, amount)
#
#
#         # Confirmation message with details
#         confirmation = (
#             f"✅ Expense Saved!\n"
#             f"📂 Category: {category}\n"
#             f"💰 Amount: {amount:.2f}"
#         )
#
#         reply_markup = ReplyKeyboardMarkup(MAIN_KEYBOARD, resize_keyboard=True)
#         await start_timer(context)
#         await update.message.reply_text(
#             confirmation,
#             reply_markup=reply_markup
#         )
#         return ConversationHandler.END
#     except ValueError:
#         await start_timer(context)
#         await update.message.reply_text("Please enter a valid positive number.")
#         return AMOUNT
#
#
#
#
#
# #
# #
# # async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
# #     reply_markup = ReplyKeyboardMarkup(MAIN_KEYBOARD, resize_keyboard=True)
# #     await start_timer(context)
# #     await update.message.reply_text(
# #         welcome_text,
# #         reply_markup=reply_markup
# #     )
# #
# # async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
# #     """Cancel the current conversation."""
# #     reply_markup = ReplyKeyboardMarkup(MAIN_KEYBOARD, resize_keyboard=True)
# #     await start_timer(context)
# #     await update.message.reply_text(
# #         "Operation canceled. What would you like to do next? 🤔",
# #         reply_markup=reply_markup
# #     )
# #     return ConversationHandler.END
# #
# # async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
# #     reply_markup = ReplyKeyboardMarkup(MAIN_KEYBOARD, resize_keyboard=True)
# #     await start_timer(context)
# #     await update.message.reply_text(help_text, reply_markup=reply_markup)
# #
# # async def add_expense_start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
# #     context.user_data.clear()  # Clear any previous conversation data
# #     types = [['Fixed Expense', 'Temporary Expense']]
# #     await start_timer(context)
# #     reply_markup = ReplyKeyboardMarkup(types, resize_keyboard=True, one_time_keyboard=True)
# #
# #     await update.message.reply_text(
# #         "Please select the type of expense (Fixed or Temporary):",
# #         reply_markup=reply_markup
# #     )
# #     return EXPENSE_TYPE
# #
# # async def get_expense_type(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
# #     type = update.message.text
# #     context.user_data["expense_type"] = type
# #     keyboard = [category for category in EXPENSE_CATEGORIES]
# #     reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=True)
# #     await start_timer(context)
# #     await update.message.reply_text(
# #         "Please select a category for your expense 📂:",
# #         reply_markup=reply_markup
# #     )
# #     return CATEGORY
# #
# # async def get_category(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
# #     category = update.message.text.split()[-1]  # Extract category without emoji
# #     context.user_data['category'] = category
# #     await start_timer(context)
# #     await update.message.reply_text(
# #         "How much was the expense? 💰\n"
# #         "(Enter the amount in your local currency)"
# #     )
# #     return AMOUNT
# #
# # async def save_expense(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
# #     """Save the expense to the database."""
# #     try:
# #         amount = float(update.message.text)
# #         if amount <= 0:
# #             raise ValueError("Amount must be positive")
# #
# #         user_id = update.effective_user.id
# #         category = context.user_data['category']
# #         type = context.user_data['expense_type']
# #
# #         if type == 'Fixed Expense':
# #             save_fixed_expenses_to_db(user_id, category, amount)
# #         elif type == 'Temporary Expense':
# #             save_temporary_expenses_to_db(user_id, category, amount)
# #
# #         # Confirmation message with details
# #         confirmation = (
# #             f"✅ Expense Saved!\n"
# #             f"📂 Category: {category}\n"
# #             f"💰 Amount: {amount:.2f}"
# #         )
# #
# #         reply_markup = ReplyKeyboardMarkup(MAIN_KEYBOARD, resize_keyboard=True)
# #         await start_timer(context)
# #         await update.message.reply_text(
# #             confirmation,
# #             reply_markup=reply_markup
# #         )
# #         return ConversationHandler.END
# #     except ValueError:
# #         await start_timer(context)
# #         await update.message.reply_text("Please enter a valid positive number.")
# #         return AMOUNT
#
#
#
import asyncio
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ContextTypes, ConversationHandler
from repository.db import save_temporary_expenses_to_db, save_fixed_expenses_to_db
from texts import help_text, EXPENSE_CATEGORIES, welcome_text, MAIN_KEYBOARD

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
        await asyncio.sleep(10)  # זמן המתנה של 10 שניות (ניתן לשינוי)
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
        pass  # ביטול המשימה יפסיק את ההמתנה ללא שגיאה

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    context.user_data['chat_id'] = update.effective_chat.id  # שמירה של chat_id ב-user_data
    reply_markup = ReplyKeyboardMarkup(MAIN_KEYBOARD, resize_keyboard=True)
    await start_timer(context)
    await update.message.reply_text(
        welcome_text,
        reply_markup=reply_markup
    )

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Cancel the current conversation."""
    reply_markup = ReplyKeyboardMarkup(MAIN_KEYBOARD, resize_keyboard=True)
    await start_timer(context)
    await update.message.reply_text(
        "Operation canceled. What would you like to do next? 🤔",
        reply_markup=reply_markup
    )
    return ConversationHandler.END

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    reply_markup = ReplyKeyboardMarkup(MAIN_KEYBOARD, resize_keyboard=True)
    await start_timer(context)
    await update.message.reply_text(help_text, reply_markup=reply_markup)

async def add_expense_start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data.clear()  # Clear any previous conversation data
    types = [["Fixed Expense", "Temporary Expense"]]
    await start_timer(context)
    reply_markup = ReplyKeyboardMarkup(types, resize_keyboard=True, one_time_keyboard=True)

    await update.message.reply_text(
        "Please select the type of expense (Fixed or Temporary):",
        reply_markup=reply_markup
    )
    return EXPENSE_TYPE

async def get_expense_type(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    expense_type = update.message.text
    context.user_data["expense_type"] = expense_type
    keyboard = [category for category in EXPENSE_CATEGORIES]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=True)
    await start_timer(context)
    await update.message.reply_text(
        "Please select a category for your expense 📂:",
        reply_markup=reply_markup
    )
    return CATEGORY

async def get_category(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    category = update.message.text.split()[-1]  # Extract category without emoji
    context.user_data['category'] = category
    await start_timer(context)
    await update.message.reply_text(
        "How much was the expense? 💰\n"
        "(Enter the amount in your local currency)"
    )
    return AMOUNT

async def save_expense(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Save the expense to the database."""
    try:
        amount = float(update.message.text)
        if amount <= 0:
            raise ValueError("Amount must be positive")

        user_id = update.effective_user.id
        category = context.user_data['category']
        expense_type = context.user_data['expense_type']

        if expense_type == 'Fixed Expense':
            save_fixed_expenses_to_db(user_id, category, amount)
        elif expense_type == 'Temporary Expense':
            save_temporary_expenses_to_db(user_id, category, amount)

        confirmation = (
            f"✅ Expense Saved!\n"
            f"📂 Category: {category}\n"
            f"💰 Amount: {amount:.2f}"
        )

        reply_markup = ReplyKeyboardMarkup(MAIN_KEYBOARD, resize_keyboard=True)
        await start_timer(context)
        await update.message.reply_text(
            confirmation,
            reply_markup=reply_markup
        )
        return ConversationHandler.END
    except ValueError:
        await start_timer(context)
        await update.message.reply_text("Please enter a valid positive number.")
        return AMOUNT
