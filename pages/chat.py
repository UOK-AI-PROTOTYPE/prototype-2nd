import streamlit as st
from openai import OpenAI
from streamlit_chat import message
from utils.chat_background import chat_background
from utils.db import add_user, get_user, add_userResult, get_user_info, get_user_result
from utils import modal
import toml
import time
from utils.result import generate_result

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

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = setting["openai_model"]

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": prompts["setting_prompt"]}
    ]

if "user_info" not in st.session_state:
    modal.signIn_modal()
else:
    if "participant" not in st.session_state:
        st.session_state.participant = []
        modal.enter_modal()

######## GPT API를 사용하여 질문을 생성하는 함수
def generate_initial_question(target_name, num_participant):
    response = client.chat.completions.create(
        model=st.session_state["openai_model"],
        messages=[
            {"role": "system", "content": prompts["setting_prompt"]},
            {"role": "assistant", "content": f"target-name :{target_name}, participant-number: {num_participant}" }
        ]
    )
    return response.choices[0].message.content
    

if 'target_name' in st.session_state and 'num_participant' in st.session_state and "remaining_users" not in st.session_state:
    target_name = st.session_state['target_name'] # 분석대상 이름
    num_participant = st.session_state['num_participant'] # 총 참여자 수
    st.session_state['remaining_users'] = st.session_state['num_participant'] - 1

    #######GPT API를 사용하여 첫 번째 질문 생성
    stream = generate_initial_question(target_name, num_participant)
    st.session_state.messages.append({"role": "assistant", "content": stream})

for message in st.session_state.messages[1:]:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

def count_user_roles(messages):
    return sum(1 for message in messages if message["role"] == "user")

# 분석완료 여부 확인
# 분석완료이면, True 리턴
def check_analysis(response):
    KEYWORDS_1 = ["MBTI", "mbti"]
    KEYWORDS_2 = ["ISTJ", "ISTP", "ISFJ", "ISFP", "INTJ", "INTP", "INFJ", "INFP", "ESTJ", "ESTP", "ESFJ", "ESFP", "ENTJ", "ENTP", "ENFJ", "ENFP", "istj", "istp", "isfj", "isfp", "intj", "intp", "infj", "infp", "estj", "estp", "esfj", "esfp", "entj", "entp", "enfj", "enfp"]

    return any(keyword in response for keyword in KEYWORDS_1) and any(keyword in response for keyword in KEYWORDS_2)

if prompt := st.chat_input("답변을 작성해주세요 !"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    # st.write(st.session_state.messages)
    # st.write(get_user_info())
    # st.write(get_user_result())

    with st.chat_message("user"):
        st.markdown(prompt)

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
    
    if check_analysis(response):
        target_name = st.session_state['target_name']
        target_id = st.session_state.user_info[0]

        if len(st.session_state.participant) == 0:  # 본인인 경우
            add_userResult(target_id, target_name, target_name, "본인", response, "")
            st.session_state.participant.append({"name": target_name, "relation": "본인", "result": response})
        else:  # 타인인 경우
            participant = st.session_state.participant[-1]
            participant_name = participant["name"]
            relation = participant["relation"]
            add_userResult(target_id, target_name, participant_name, relation, response, "")
            st.session_state.participant[-1]["result"] = response

        if st.session_state['remaining_users'] == 0:    # 마지막 유저 (남아있는 인원 : 0)
            # TODO : 완성본의 경우 최종결과 여기서 받아오도록 수정
            # st.session_state.final_result = generate_result()
            time.sleep(2)
            modal.end_modal(response)
        else:
            st.session_state['remaining_users'] -= 1
            time.sleep(2)
            modal.user_change(target_name)
