import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), 'bot.db')

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            credits INTEGER DEFAULT 3,
            is_premium BOOLEAN DEFAULT 0
        )
    ''')
    conn.commit()
    conn.close()

def get_user(user_id: int):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('SELECT credits, is_premium FROM users WHERE user_id = ?', (user_id,))
    row = c.fetchone()
    if not row:
        c.execute('INSERT INTO users (user_id) VALUES (?)', (user_id,))
        conn.commit()
        row = (3, False)
    conn.close()
    return {"credits": row[0], "is_premium": bool(row[1])}

def consume_credit(user_id: int) -> bool:
    user = get_user(user_id)
    if user["is_premium"]:
        return True
    if user["credits"] > 0:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute('UPDATE users SET credits = credits - 1 WHERE user_id = ?', (user_id,))
        conn.commit()
        conn.close()
        return True
    return False

def add_credits(user_id: int, amount: int):
    get_user(user_id) # ensure exists
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('UPDATE users SET credits = credits + ? WHERE user_id = ?', (amount, user_id))
    conn.commit()
    conn.close()

def upgrade_user(user_id: int):
    get_user(user_id) # ensure exists
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('UPDATE users SET is_premium = 1 WHERE user_id = ?', (user_id,))
    conn.commit()
    conn.close()
