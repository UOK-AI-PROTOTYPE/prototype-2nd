import streamlit as st
from openai import OpenAI
from streamlit_chat import message
from streamlit_navigation_bar import st_navbar
from utils.chat_background import chat_background
from intro import set_intro
import toml, json

st.set_page_config(
    initial_sidebar_state="collapsed",
    page_title="UOK AI PROJECT",
    page_icon="🤖",
    layout="centered",
)

setting = toml.load('setting.toml')
prompts = toml.load('prompts.toml')
json_styles = 'styles.json'


pages = ["ChatBot", "UOK"]
urls = {"UOK": setting["urls"]}
logos = setting["page_icon"]
with open(json_styles, 'r') as file:
    styles = json.load(file)

page = st_navbar(
    pages,
    urls=urls,
    styles=styles,
    options={"show_menu": True, "use_padding": True,}
)
st.write(page)


# with st.sidebar:
#     st.image(logos, width=70)
#     st.write(prompts["sidebar_script"])
st.title("UOK 성향 추론 챗봇")
st.write("챗봇과의 대화를 통해 사용자의 성향을 파악할 수 있습니다. 지금 바로 대화를 나눠보세요!")

# chat_background()

#_____________________________________________________

st.markdown(
    """
    <style>
    .user-message {
        background-color: #ACB9FE, 28%;
        color: #0f5132;
        padding: 10px;
        border-radius: 5px;
        margin-bottom: 10px;
    }
    .assistant-message {
        background-color: #2A3EAA, 16%;
        color: #842029;
        padding: 10px;
        border-radius: 5px;
        margin-bottom: 10px;
    }
    </style>
    """,
    unsafe_allow_html=True
)












client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = setting["openai_model"]

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": prompts["setting_prompt"]}
    ]

with st.chat_message("assistant"):
    st.markdown(prompts["first_prompt"])

for message in st.session_state.messages[1:]:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

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
            stream=True,
        )
        response = st.write_stream(stream)
    st.session_state.messages.append({"role": "assistant", "content": response})
