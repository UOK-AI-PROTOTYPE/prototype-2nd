# db.py
import sqlite3
from contextlib import closing

DATABASE = './test.db'

def create_table():
    with closing(sqlite3.connect(DATABASE)) as conn:
        with conn as cur:
            # userInfo 테이블
            cur.execute('''
                CREATE TABLE IF NOT EXISTS userInfo (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    email TEXT UNIQUE,
                    username TEXT NOT NULL,
                    hashed_password TEXT,
                    age TEXT,
                    gender TEXT   
                )
            ''')
            # userResult 테이블
            cur.execute('''
                CREATE TABLE IF NOT EXISTS userResult (
                    id INTEGER PRIMARY KEY,
                    target_name INTEGER NOT NULL,
                    participant_name INTEGER NOT NULL,
                    relationship TEXT,
                    result TEXT
                )
            ''')
            # 변경사항 저장
            conn.commit()

def add_user(email, username, hashed_password):
    with closing(sqlite3.connect(DATABASE)) as conn:
        with conn as cur:
            cur.execute('INSERT INTO userInfo (email, username, hashed_password) VALUES (?, ?, ?)', (email, username, hashed_password))

def get_user(email):
    with closing(sqlite3.connect(DATABASE)) as conn:
        with closing(conn.cursor()) as cur:
            cur.execute('SELECT * FROM userInfo WHERE email= ?', (email,))
            return cur.fetchone()
        
def get_user_info():
    with closing(sqlite3.connect(DATABASE)) as conn:
        with closing(conn.cursor()) as cur:
            cur.execute('SELECT * FROM userInfo')
            return cur.fetchall()

def get_user_result():
    with closing(sqlite3.connect(DATABASE)) as conn:
        with closing(conn.cursor()) as cur:
            cur.execute('SELECT * FROM userResult')
            return cur.fetchall()
 
    
create_table()
