import streamlit as st

# 챗봇 입장시
@st.experimental_dialog("분석 대상자의 정보를 알려주세요 !")
def enter_modal():
    target_name = st.text_input("분석대상의 이름을 입력해주세요")
    num_participant = st.number_input("총 참여자 수를 입력해주세요", min_value=1, value=None)
    if st.button("제출", type="primary"):
        if target_name and num_participant:
            st.session_state['target_name'] = target_name
            st.session_state['num_participant'] = num_participant
            # st.switch_page("pages/chat.py")
            st.rerun()
        else:
            st.warning("모든 항목을 입력해주세요.")
            
# 사용자 전환시
@st.experimental_dialog("""이제부터는 지인이 대화할 차례에요 !
                        이름과 관계를 알려주세요.""")
def user_change(target_name, response):
    st.markdown(response)
    new_user_name = st.text_input("이름을 입력해주세요")
    new_user_relation = st.selectbox(
        f"{target_name}님과의 관계는?",
        options=("가족", "친구", "친척", "동료", "기타"),
        index=None,
        placeholder="관계를 설정해주세요"
    )
    if st.button("분석 시작하기", type="primary"):
        if new_user_name and new_user_relation:
            # user_info에 새 사용자의 이름, 관계 저장
            st.session_state.user_info.append({"name": new_user_name, "relation": new_user_relation})
            st.session_state.messages.append({"role": "assistant", "content": 
                f"""안녕하세요, {new_user_name}님.
                {target_name}님과 {new_user_relation} 관계이시군요!
                그럼 이제 {target_name}님에 대해 질문 드리겠습니다. 평소 {target_name}님은 어떤 캐릭터인가요?"""})
            st.rerun()
        else:
            st.warning("모든 항목을 입력해주세요.")

# 모든 분석 종료시
@st.experimental_dialog("분석이 모두 끝났습니다 !")
def end_modal(result):
    # st.markdown(result)
    st.session_state.result = result
    if st.button("분석 결과 보러가기", type="primary"):
        st.switch_page("pages/result.py")


# UserChange
# @st.experimental_dialog("이제부터는 지인이 대화할 차례에요 !")
# def userChange(target_name):
#     user_name = st.text_input("이름을 입력해주세요")
#     user_relation = st.selectbox(
#         f"{target_name}님과의 관계는?",
#         options=("가족", "친구", "친척", "동료", "기타"),
#         index=None,
#         placeholder="관계 설정 고고링"
#     )

#     if st.button("분석 시작하기", type="primary"):
#         if user_name and user_relation:
#             st.session_state['user_name'] = user_name
#             st.session_state['user_relation'] = user_relation
#             st.session_state.messages.append({
#                 "role": "user",
#                 "content": f"{user_name}: {user_relation}"
#             })
#             st.rerun
#         else:
#             st.warning("모든 항목을 입력해주세요.")