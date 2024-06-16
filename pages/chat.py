import streamlit as st
from openai import OpenAI
from streamlit_chat import message
from utils.chat_background import chat_background
from utils import modal
import toml

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


if "user_info" not in st.session_state:
    modal.signIn_modal()
else:
    if "ex" not in st.session_state: #이 부분 수정 필요
        st.session_state['ex']=0
        modal.enter_modal()

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": prompts["setting_prompt"]}
    ]
    # modal.enter_modal()


# first_question이 답변할 때마다 출력되는 문제 해결
if 'target_name' in st.session_state and 'num_participant' in st.session_state and "remaining_users" not in st.session_state:
    target_name = st.session_state['target_name'] # 분석대상 이름
    num_participant = st.session_state['num_participant'] # 총 참여자 수
    st.session_state['remaining_users'] = st.session_state['num_participant']

    # 첫번째 질문 (하드코딩)
    first_question = f"""안녕하세요, {target_name}님.
    총 {num_participant}분이 MBTI분석에 참여하시는군요.:) 
    첫번째 질문드리겠습니다.  
    가장 선호하는 영화와 그 이유, 또는 가장 선호하는 장면을 알려주세요."""

    # 첫번째 질문 messages에 추가
    st.session_state.messages.append({"role": "assistant", "content": first_question})
    print(st.session_state.messages)


for message in st.session_state.messages[1:]:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.markdown(message["content"])   


def count_user_roles(messages):
    return sum(1 for message in messages if message["role"] == "user")
    
# 분석완료 여부 확인
# 분석완료이면, True 리턴
def check_analysis(response):
    KEYWORDS_1 = ["MBTI","mbti"]
    KEYWORDS_2 = [ "ISTJ", "ISTP", "ISFJ", "ISFP", "INTJ", "INTP", "INFJ", "INFP", "ESTJ", "ESTP", "ESFJ", "ESFP", "ENTJ", "ENTP", "ENFJ", "ENFP", "istj", "istp", "isfj", "isfp", "intj", "intp", "infj", "infp", "estj", "estp", "esfj", "esfp", "entj", "entp", "enfj", "enfp"]
    
    return any(keyword in response for keyword in KEYWORDS_1) and any(keyword in response for keyword in KEYWORDS_2)


if prompt := st.chat_input("답변을 작성해주세요 !"):
    st.session_state.messages.append({"role": "user", "content": prompt})

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
        if st.session_state['remaining_users'] == 1:
            modal.end_modal(response)
        else:
            st.session_state['remaining_users'] -= 1
            modal.user_change(target_name, response)