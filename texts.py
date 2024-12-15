EXPENSE_CATEGORIES = [
    ['🍽️ Food', '🚗 Transport', '🏠 Rent/Utilities'],
    ['🛒 Groceries', '👗 Shopping', '🎉 Entertainment'],
    ['🏥 Health', '📚 Education', '🚌 Public Transit'],
    ['🎁 Gifts', '💻 Technology', '🍺 Dining Out'],
    ['🏋️ Fitness', '✈️ Travel', 'Other'],
    ['❌ Cancel']
]

help_text = (
    "Expense Tracker Bot Help 🆘\n\n"
    "🔹 Add Expense: Record your daily expenses\n"
    "🔹 Report: View your spending summary\n"
    "🔹 Categories: Food, Transport, Rent, Groceries, Shopping, etc.\n\n"
    "Tips:\n"
    "- Use numeric values for expense amounts\n"
    "- Choose the most relevant category"
)

CATEGORY_MAPPING = {
    '🍽️ Food': 'Food',
    '🚗 Transport': 'Transport',
    '🏠 Rent/Utilities': 'Rent/Utilities',
    '🛒 Groceries': 'Groceries',
    '👗 Shopping': 'Shopping',
    '🎉 Entertainment': 'Entertainment',
    '🏥 Health': 'Health',
    '📚 Education': 'Education',
    '🚌 Public Transit': 'Public Transit',
    '🎁 Gifts': 'Gifts',
    '💻 Technology': 'Technology',
    '🍺 Dining Out': 'Dining Out',
    '🏋️ Fitness': 'Fitness',
    '✈️ Travel': 'Travel',
    'Other': 'Other'
}
welcome_text = ("Welcome to Expense Tracker Bot! 💰\n\n"
        "Track your expenses easily and get insights into your spending.\n"
        "Choose an option below to get started.")

MAIN_KEYBOARD = [["💸 Add Expense","💰 Add Income" ], ["❓ Help", "📊 Report"],["Search News"]]