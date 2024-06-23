import streamlit as st
from utils.db import add_user, get_user, add_userResult
import bcrypt
from openai import OpenAI
from streamlit_chat import message
import toml

def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))

def generate_question(target_name, participant_name, relation):
    messages=[ 
        {"role": m["role"], "content": m["content"]}
        for m in st.session_state.messages
    ].copy()
    messages.append({
        "role": "assistant", 
        "content": 
            f"""target_name: {target_name}, participant_name :{participant_name}, relation: {relation},
            이제 분석대상인 {target_name}에 대해서 {relation} 관계인 {participant_name}가 대화에 참여할거야.
            안녕하세요 {participant_name}님, {target_name}과 {relation} 관계이시군요!☺️ 라는 문장을 답변에 필수로 포함하고 분석을 진행해줘."""
            })

    response = client.chat.completions.create(
        model=st.session_state["openai_model"],
        messages=messages
    )
    return response.choices[0].message.content


client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
prompts = toml.load('static/toml/prompts.toml')


# 챗봇 입장시 :  로그인 모달과 연계되는 모달 - 수정 버전
@st.experimental_dialog("분석에 참여할 인원을 알려주세요 ☺️ ")
def enter_modal():
    target_id, target_name = st.session_state.user_info[0], st.session_state.user_info[1]
    st.subheader(f"안녕하세요, {target_name}님.")
    num_participant = st.number_input("총 참여자 수를 입력해주세요", min_value=1, value=None)
    if st.button("제출", type="primary"):
        if target_name and num_participant:
            st.session_state['target_name'] = target_name
            st.session_state['num_participant'] = num_participant      
            st.rerun()
        else:
            st.warning("모든 항목을 입력해주세요.")


# end_modal
@st.experimental_dialog("분석이 모두 끝났습니다 !")
def end_modal(result):
    st.session_state.result = result
    if st.button("분석 결과 보러가기", type="primary"):
        st.switch_page("pages/result.py")
        



# 대상자 본인 채팅 이후 차례에서 뜨는 모달 - 수정버전(gpt api가 첫질문)
@st.experimental_dialog("""이제부터는 지인이 대화할 차례에요 !
                        이름과 관계를 알려주세요.""")
def user_change(target_name):
    participant_name = st.text_input("이름을 입력해주세요")
    relation = st.selectbox(
        f"{target_name}님과의 관계는?",
        options=("가족", "친구", "친척", "동료", "기타"),
        index=None,
        placeholder="관계를 설정해주세요"
    )

    if st.button("분석 시작하기", type="primary"):
        st.session_state.participant.append({"name": participant_name, "relation": relation, "result": None})
        stream = generate_question(target_name, participant_name, relation)
        st.session_state.messages.append({"role": "assistant", "content": stream})
        st.rerun()
    return participant_name, relation





# 로그인 모달
@st.experimental_dialog("로그인 후 서비스를 이용해주세요 🥹")
def signIn_modal():
    email = st.text_input("Email", placeholder="이메일을 입력해주세요")
    password = st.text_input("Password", placeholder="비밀번호를 입력해주세요", type="password")

    st.markdown("""
        <style>
        .stButton button {
            height: 2.8rem;
            margin-top: 0.4rem;
        }
        </style>
    """, unsafe_allow_html=True)

    if st.button("로그인", use_container_width=True, type="primary"):
        user = get_user(email)
        if user and verify_password(password, user[3]):   
            target_id, target_name = user[0], user[2]
            
            # 사용자들의 정보(이름, 관계)를 user_info에 저장
            if "user_info" not in st.session_state: #[user_info]=[타겟id, 타겟이름]
                st.session_state["user_info"] = [target_id, target_name]
            st.success(f"{target_name}님, 로그인 성공!")
            st.rerun()
        else:
            st.error("로그인 실패. 사용자명 또는 비밀번호를 확인하세요.")
    if st.button("회원가입", use_container_width=True):
        st.switch_page("pages/sign_up.py")
