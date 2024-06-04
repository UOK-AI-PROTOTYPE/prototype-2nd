import streamlit as st
from openai import OpenAI
from streamlit_chat import message
from streamlit_navigation_bar import st_navbar
from utils.background import set_background
import toml, json

setting = toml.load('setting.toml')
prompts = toml.load('prompts.toml')
json_styles = 'styles.json'

st.set_page_config(
    initial_sidebar_state="collapsed",
    page_title="UOK AI PROJECT",
    page_icon=setting["page_icon"],
    layout="wide",
)

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

set_background()

with st.sidebar:
    st.image(logos, width=70)
    st.write(prompts["sidebar_script"])
st.title("UOK 성향 추론 챗봇")
st.write("챗봇과의 대화를 통해 사용자의 성향을 파악할 수 있습니다. 지금 바로 대화를 나눠보세요!")


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
