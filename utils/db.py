# db.py
import sqlite3
from contextlib import closing

DATABASE = './test.db'

def create_table():
    with closing(sqlite3.connect(DATABASE)) as conn:
        with conn as cur:
            cur.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    email TEXT UNIQUE,
                    username TEXT,
                    hashed_password TEXT,
                    age TEXT,
                    gender TEXT   
                )
            ''')

def add_user(email, hashed_password):
    with closing(sqlite3.connect(DATABASE)) as conn:
        with conn as cur:
            cur.execute('INSERT INTO users (email, hashed_password) VALUES (?, ?)', (email, hashed_password))

def get_user(email):
    with closing(sqlite3.connect(DATABASE)) as conn:
        with closing(conn.cursor()) as cur:
            cur.execute('SELECT * FROM users WHERE eamil= = ?', (email,))
            return cur.fetchone()

create_table()
