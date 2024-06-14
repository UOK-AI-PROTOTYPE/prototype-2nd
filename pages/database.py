import streamlit as st
from openai import OpenAI
from streamlit_chat import message
from utils.chat_background import chat_background
import utils.connection as db_conn
from utils import modal
import toml

conn, cursor = db_conn.create_connection()  # 데이터베이스 연결 및 테이블 생성
user_info_rows, user_result_rows = db_conn.fetch_data(cursor)  # 데이터 조회 및 출력

setting = toml.load('static/toml/setting.toml')
prompts = toml.load('static/toml/prompts.toml')

st.set_page_config(
    initial_sidebar_state="collapsed",
    page_title="UOK AI PROJECT",
    page_icon=setting["page_icon"],
    layout="centered",
)

chat_background()
st.title("UOK 성향 추론 챗봇")
st.write("챗봇과의 대화를 통해 사용자의 성향을 파악할 수 있습니다. 지금 바로 대화를 나눠보세요!")

####### 데이터 출력
st.write("userInfo 테이블 데이터:", user_info_rows)
st.write("userResult 테이블 데이터:", user_result_rows)

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = setting["openai_model"]

if "conversation_count" not in st.session_state:
    st.session_state["conversation_count"] = 0

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": prompts["setting_prompt"]}
    ]
    modal.enter_modal()

# first_question이 답변할 때마다 출력되는 문제 해결
if 'target_name' in st.session_state and 'num_participant' in st.session_state and "start" not in st.session_state:
    target_name = st.session_state['target_name'] # 분석대상 이름
    num_participant = st.session_state['num_participant'] # 총 참여자 수
    st.session_state.start = []

    # 첫번째 질문 (하드코딩)
    first_question = f"""안녕하세요, {target_name}님.
    총 {num_participant}분이 MBTI분석에 참여하시는군요.:) 
    첫번째 질문드리겠습니다.  
    가장 선호하는 영화와 그 이유, 또는 가장 선호하는 장면을 알려주세요."""

    # 첫번째 질문 messages에 추가
    st.session_state.messages.append({"role": "assistant", "content": first_question})

for message in st.session_state.messages[1:]:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.markdown(message["content"])   

def count_user_roles(messages):
    return sum(1 for message in messages if message["role"] == "user")

if prompt := st.chat_input("답변을 작성해주세요 !"):
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("user"):
        st.markdown(prompt)

    if count_user_roles(st.session_state.messages) == 3:
        target_name = st.session_state['target_name']
        num_participant = st.session_state['num_participant'] # 총 참여자 수
        modal.user_change(target_name, num_participant)
    else:
        with st.chat_message("assistant"):
            stream = client.chat.completions.create(
                model=st.session_state["openai_model"],
                max_tokens=1000, # 생성할 최대 토큰 수
                temperature = 1,  # 다양성 조절을 위한 온도 매개변수
                presence_penalty= 1.5, # 값이 클수록 새로운 주제에 대해 이야기
                messages=[ 
                    {"role": m["role"], "content": m["content"]}
                    for m in st.session_state.messages
                ],
                stream=True
            )
            response = st.write_stream(stream)
        st.session_state.messages.append({"role": "assistant", "content": response})
