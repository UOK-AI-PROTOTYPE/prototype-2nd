import streamlit as st


@st.experimental_dialog("분석 대상자의 정보를 알려주세요 !")
def trigger1():
    user_name = st.text_input("이름을 입력해주세요")
    user_relation = st.selectbox(
        "관계는?",
        options=("본인", "가족", "친구", "친척", "동료"),
        index=None,
        placeholder="관계 설정 고고링"
    )
    if st.button("분석 시작하기"):
        st.session_state.messages.append({"role": "user", "content": user_relation, "userInfo": user_name})
        # st.session_state.relation = {"name": user2_name, "relation": user2_relation}
        # print(st.session_state.messages)
        st.rerun()


@st.experimental_dialog("이제부터는 00님의 지인이 대화할 차례에요 !")
def trigger2():
    user2_name = st.text_input("이름을 입력해주세요")
    user2_relation = st.selectbox(
        "00님과의 관계는?",
        options=("본인", "가족", "친구", "친척", "동료"),
        index=None,
        placeholder="관계 설정 고고링"
    )
    if st.button("분석 시작하기"):
        st.session_state.messages.append({"role": "user", "content": user2_relation, "userInfo": user2_name})
        # st.session_state.relation = {"name": user2_name, "relation": user2_relation}
        # print(st.session_state.messages)
        st.rerun()