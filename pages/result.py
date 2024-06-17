import streamlit as st
from openai import OpenAI
from streamlit_chat import message
from utils import modal
import re

def find_mbti(result):
    mbti_pattern = re.compile(r'MBTI\s*:\s*([A-Z]{4})')
    mbti_match = mbti_pattern.search(result)
    mbti = mbti_match.group(1) if mbti_match else None

    ratio_pattern = re.compile(r'([A-Z])\s*\(.*?\):\s*(\d+)%')
    ratios = {match.group(1): int(match.group(2)) for match in ratio_pattern.finditer(result)}

    return mbti, ratios

for data in st.session_state.participant:
    mbti, ratios = find_mbti(data["result"])
    st.markdown(f"{data['name']}님의 분석결과")
    st.markdown(f"MBTI: {mbti}")
    st.markdown("비율:")
    for key, value in ratios.items():
        st.markdown(f"{key}: {value}%")
     

if st.button("다시 분석 하러가기", type="primary"):
    # st.session_state의 특정값들을 삭제해서 chat 페이지로 돌아갔을 때, 상태 초기화
    del st.session_state.messages
    del st.session_state['remaining_users']
    del st.session_state.user_data

    st.switch_page("pages/chat.py")