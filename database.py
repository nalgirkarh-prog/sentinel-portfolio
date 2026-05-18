import sqlite3
import os

DB_PATH = "data/portfolio.db"

def init_db():
    os.makedirs("data", exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS portfolio (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ticker TEXT NOT NULL UNIQUE,
            quantity INTEGER NOT NULL,
            avg_buy_price REAL NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def get_portfolio():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT ticker, quantity, avg_buy_price FROM portfolio")
    rows = cursor.fetchall()
    conn.close()
    return [{"ticker": r[0], "quantity": r[1], "avg_buy_price": r[2]} for r in rows]

init_db()
