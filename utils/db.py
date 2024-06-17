# db.py
import sqlite3
from contextlib import closing

DATABASE = './test.db'

def create_table():
    with closing(sqlite3.connect(DATABASE)) as conn:
        with conn as cur:
            # userInfo 테이블 : id, 이메일, 이름, 비번, 연령대, 성별
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
            # userResult 테이블 : id, 타겟id, 타겟이름, 지인id, 지인이름, 관계, 결과
            # 지인도 계정이 연동되어야한다면 participant_id INTEGER NOT NULL, 이 추가되어야함
            #E70S50T60P65 형식, 필요시 수정
            cur.execute('''
                CREATE TABLE IF NOT EXISTS userResult (
                    id INTEGER PRIMARY KEY,
                    target_id INTEGER NOT NULL,
                    target_name TEXT NOT NULL,
                    participant_name TEXT NOT NULL,
                    relation TEXT,
                    result TEXT,
                    mbti TEXT 
                )
            ''')
            # 변경사항 저장
            conn.commit()

# 유저 정보 조회
def get_user(email):
    with closing(sqlite3.connect(DATABASE)) as conn:
        with closing(conn.cursor()) as cur:
            cur.execute('SELECT * FROM userInfo WHERE email= ?', (email,))
            return cur.fetchone()

# 유저 정보 저장
def add_user(email, username, hashed_password):
    with closing(sqlite3.connect(DATABASE)) as conn:
        with conn as cur:
            cur.execute('INSERT INTO userInfo (email, username, hashed_password) VALUES (?, ?, ?)', (email, username, hashed_password))

# 유저 분석 결과 저장
# userResult 테이블 : id, 타겟id, 타겟이름, 지인이름, 관계, 결과
def add_userResult(target_id, target_name, participant_name, relation, result, mbti):
    with closing(sqlite3.connect(DATABASE)) as conn:
        with conn as cur:
            cur.execute('INSERT INTO userResult (target_id, target_name, participant_name, relation, result, mbti) VALUES (?, ?, ?, ?, ?, ?)', (target_id, target_name, participant_name, relation, result, mbti))

# # 이메일로 유저 분석 결과 조회
# def get_user_result_by_email(email):
#     with closing(sqlite3.connect(DATABASE)) as conn:
#         with closing(conn.cursor()) as cur:
#             # 이메일로 유저 조회
#             cur.execute('SELECT id FROM userInfo WHERE email = ?', (email,))
#             user = cur.fetchone()
#             if user:
#                 user_id = user[0]
#                 # 해당 유저의 분석 결과 조회
#                 cur.execute('SELECT * FROM userResult WHERE target_id = ?', (user_id,))
#                 return cur.fetchall()
#             else:
#                 return None

# 유저 정보 전체 조회
def get_user_info():
    with closing(sqlite3.connect(DATABASE)) as conn:
        with closing(conn.cursor()) as cur:
            cur.execute('SELECT * FROM userInfo')
            return cur.fetchall()

# 유저 분석 결과 전체 조회
def get_user_result():
    with closing(sqlite3.connect(DATABASE)) as conn:
        with closing(conn.cursor()) as cur:
            cur.execute('SELECT * FROM userResult')
            return cur.fetchall()
 
    
create_table()
