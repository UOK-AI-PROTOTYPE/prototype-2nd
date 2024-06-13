import streamlit as st
import bcrypt
from utils.db import add_user, get_user
from utils.chat_background import chat_background

def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))


# 로그인 모달
@st.experimental_dialog("로그인 후 서비스를 이용해주세요 🥹")
def signIn_modal():
    email = st.text_input("Email", placeholder="이메일을 입력해주세요")
    password = st.text_input("Password", placeholder="비밀번호를 입력해주세요", type="password")

    st.markdown("""
        <style>
        .stButton button {
            height: 2.8rem;
            margin-top: 1.5rem;
        }
        </style>
    """, unsafe_allow_html=True)

    if st.button("로그인", use_container_width=True, type="primary"):
        user = get_user(email)
        if user and verify_password(password, user[3]):
            st.success(f"{email}님, 로그인 성공!")
            st.switch_page("pages/database.py")
        else:
            st.error("로그인 실패. 사용자명 또는 비밀번호를 확인하세요.")
    
    if st.button("회원가입", use_container_width=True):
        st.switch_page("pages/sign_up.py")




        # 글씨에 링크 입혀서 오른쪽 정렬
        # st.markdown(f"""
        #     <div style="display: flex; justify-content: flex-end;">
        #         <a href="{sign_up_url}" target="_self" style="text-decoration: none;">
        #             <h4>회원가입</h4>
        #         </a>
        #     </div>
        # """, unsafe_allow_html=True)