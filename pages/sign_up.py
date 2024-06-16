import streamlit as st
import bcrypt
from utils.db import add_user, get_user
from utils.chat_background import chat_background
import sqlite3

def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))

chat_background()

st.title("회원가입")

email = st.text_input("이메일")
username = st.text_input("사용자명")
password = st.text_input("비밀번호", type="password")
confirm_password = st.text_input("비밀번호 재확인", type="password")
age = st.selectbox(
    "연령대",
    ("10대", "20대", "30대", "40대", "50대"),
    index=None,
    placeholder="연령대 선택하기"
)
gender = st.selectbox(
    "성별",
    ("여성", "남성"),
    index=None,
    placeholder="성별 선택하기"
)

st.markdown("""
    <style>
    .stButton button {
        float: right;
    }
    </style>
""", unsafe_allow_html=True)

if st.button("회원가입"):
    if email and password and confirm_password:
        if password == confirm_password:
            hashed_password = hash_password(password)
            try:
                add_user(email, username, hashed_password)
                st.success(f"환영합니다, {username}님!")
                st.switch_page("pages/database.py")
            except sqlite3.IntegrityError:
                st.error("이미 존재하는 이메일입니다.")
        else:
            st.error("비밀번호가 일치하지 않습니다.")
    else:
        st.error("모든 필드를 입력하세요.")