import streamlit as st
import sqlite3
from utils.db import add_user, get_user, add_userResult

conn = sqlite3.connect('example.db') #DB연결
cursor = conn.cursor()  # 커서 객체 생성

# # 챗봇 입장시
# @st.experimental_dialog("분석 대상자의 정보를 알려주세요 !")
# def enter_modal():
#     target_name = st.text_input("분석대상의 이름을 입력해주세요")
#     num_participant = st.number_input("총 참여자 수를 입력해주세요", min_value=1, value=None)
#     if st.button("제출", type="primary"):
#         if target_name and num_participant:
#             st.session_state['target_name'] = target_name
#             st.session_state['num_participant'] = num_participant
#             # st.switch_page("pages/chat.py")
#             cursor.execute(f'''
#                 INSERT INTO userInfo (name, num_participant)
#                 VALUES ('{target_name}', '{num_participant}')
#             ''')
#             conn.commit()
#             st.rerun()
#         else:
#             st.warning("모든 항목을 입력해주세요.")


@st.experimental_dialog("분석 대상자의 정보를 알려주세요 !")
def enter_modal():
    target_name = st.text_input("분석대상의 이름을 입력해주세요")
    num_participant = st.number_input("총 참여자 수를 입력해주세요", min_value=1, value=None)
    if st.button("제출", type="primary"):
        if target_name and num_participant:
            st.session_state['target_name'] = target_name
            st.session_state['num_participant'] = num_participant
            # st.switch_page("pages/chat.py")
            # cursor.execute(f'''
            #     INSERT INTO userInfo (name, num_participant)
            #     VALUES ('{target_name}', '{num_participant}')
            # ''')
            # conn.commit()
            st.rerun()
        else:
            st.warning("모든 항목을 입력해주세요.")


# 로그인 모달과 연계되는 모달 - 수정 버전
@st.experimental_dialog("분석에 참여할 인원을 알려주세요 !")
def enter_modal2():
    target_id, target_name = st.session_state.user_info[0], st.session_state.user_info[1]
    st.subheader(f"안녕하세요, {target_name}님.")
    num_participant = st.number_input("총 참여자 수를 입력해주세요", min_value=1, value=None)
    if st.button("제출", type="primary"):
        if target_name and num_participant:
            st.session_state['target_name'] = target_name
            st.session_state['num_participant'] = num_participant
            # DB에 참여인원을 저장할 필요?
            # add_userResult(target_id, target_name, target_id, target_name, "self", "")
            st.rerun()
        else:
            st.warning("모든 항목을 입력해주세요.")
            
# 사용자 전환시
@st.experimental_dialog("""이제부터는 지인이 대화할 차례에요 !
                        이름과 관계를 알려주세요.""")
def user_change(target_name, num_participant):
    user2_name = st.text_input("이름을 입력해주세요")
    user2_relation = st.selectbox(
        f"{target_name}님과의 관계는?",
        options=("가족", "친구", "친척", "동료", "기타"),
        index=None,
        placeholder="관계를 설정해주세요"
    )

    if st.button("분석 시작하기"):
        st.session_state.messages.append({"role": "assistant", "content": 
            f"""안녕하세요, {user2_name}님.
            {target_name}님과 {user2_relation} 관계이시군요!
            그럼 이제 {target_name}님에 대해 질문 드리겠습니다. 평소 {target_name}님은 어떤 캐릭터인가요?"""})
        # 현재 대상자 본인이 답변한 후 모달이 뜨는 경우의 분석 결과값을 저장하지 못함
        # -> 추후 첫번째 모달인 경우 ~ 또는 데이터베이스의 키값이 대상자인 경우~ 등으로 추가 구현해야함
        cursor.execute(f'''
            INSERT INTO userResult (target_name, participant_name, relationship)
            VALUES ('{target_name}', '{user2_name}', {user2_relation})
        ''')
        conn.commit()
        st.rerun()