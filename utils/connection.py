import sqlite3

def create_connection():
    conn = sqlite3.connect('example.db')  # 데이터베이스 연결 (파일이 존재하지 않으면 새로 생성됨)
    cursor = conn.cursor()  # 커서 객체 생성

    # 테이블 저장
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS userInfo (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            num_participant TEXT NOT NULL
        )
    ''')
    conn.commit()  # 변경 사항 저장
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS userResult (
            id INTEGER PRIMARY KEY,
            target_name INTEGER NOT NULL,
            participant_name INTEGER NOT NULL,
            relationship TEXT,
            result TEXT
        )
    ''')
    conn.commit()  # 변경 사항 저장

    return conn, cursor

def fetch_data(cursor):
    # 데이터 조회 및 출력
    cursor.execute('SELECT * FROM userInfo')
    user_info_rows = cursor.fetchall()

    cursor.execute('SELECT * FROM userResult')
    user_result_rows = cursor.fetchall()

    return user_info_rows, user_result_rows
