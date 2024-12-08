import sqlite3


def setup_database():
    conn = sqlite3.connect('expenses.db')
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS expenses (
        id INTEGER PRIMARY KEY,
        user_id INTEGER,
        category TEXT,
        amount REAL,
        date DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    conn.commit()
    conn.close()

def create_report(user_id):
    conn = sqlite3.connect('expenses.db')
    cursor = conn.cursor()

    # Total expenses by category
    cursor.execute('''
            SELECT category, 
                   SUM(amount) as total_amount, 
                   COUNT(*) as transaction_count 
            FROM expenses 
            WHERE user_id = ? 
            GROUP BY category 
            ORDER BY total_amount DESC
        ''', (user_id,))

    results = cursor.fetchall()
    conn.close()
    return results

def save_expense_to_db(user_id, category, amount):
    conn = sqlite3.connect('expenses.db')
    cursor = conn.cursor()
    cursor.execute(
        'INSERT INTO expenses (user_id, category, amount) VALUES (?, ?, ?)',
        (user_id, category, amount)
    )
    conn.commit()
    conn.close()