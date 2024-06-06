import streamlit as st
import streamlit.components.v1 as components

# 챗봇 입장시
@st.experimental_dialog("분석 대상자의 정보를 알려주세요 !")
def enter_modal():
    with st.form("input_form"):
        target_name = st.text_input("분석대상의 이름을 입력해주세요")
        num_participant = st.number_input("총 참여자 수를 입력해주세요", min_value=1, value=None)
        submit_button = st.form_submit_button(label='제출')
    
    if submit_button:
        if target_name and num_participant:
            st.session_state['target_name'] = target_name
            st.session_state['num_participant'] = num_participant
            st.switch_page("pages/chat.py")
        else:
            st.warning("모든 항목을 입력해주세요.")
            

# @st.experimental_dialog("이제부터는 00님의 지인이 대화할 차례에요 !")
# def trigger2():
#     user2_name = st.text_input("이름을 입력해주세요")
#     user2_relation = st.selectbox(
#         "00님과의 관계는?",
#         options=("본인", "가족", "친구", "친척", "동료"),
#         index=None,
#         placeholder="관계 설정 고고링"
#     )
#     if st.button("분석 시작하기"):
#         st.session_state.messages.append({"role": "user", "content": user2_relation, "userInfo": user2_name})
#         # st.session_state.relation = {"name": user2_name, "relation": user2_relation}
#         # print(st.session_state.messages)
#         st.rerun()