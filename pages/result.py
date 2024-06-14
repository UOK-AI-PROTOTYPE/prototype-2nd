import streamlit as st
from streamlit_chat import message
from utils import modal

if "result" in st.session_state:
    result = st.session_state.result

st.markdown(result)

if st.button("다시 분석 하러가기", type="primary"):
    # st.session_state의 특정값들을 삭제해서 chat 페이지로 돌아갔을 때, 상태 초기화
    del st.session_state.messages
    del st.session_state['remaining_users']

    st.switch_page("pages/chat.py")