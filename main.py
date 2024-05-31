import streamlit as st
from openai import OpenAI
from streamlit_chat import message
from streamlit_navigation_bar import st_navbar
import toml

setting = toml.load('setting.toml')
setting_pr = toml.load('setting_prompt.toml')

st.set_page_config(
    initial_sidebar_state="collapsed",
    page_title="UOK AI PROJECT",
    page_icon=setting["page_icon"],
    layout="wide",
)

pages = ["ChatBot", "UOK"]
urls = {"UOK": setting["urls"]}
logos = setting["page_icon"]
styles = {
    "nav": {
        "background-color": "rgb(42, 62, 170)",
        "text-align": "left",
    },
    "div": {
        "text-align": "left",
        "max-width": "10rem",
    },
    "img": {
        "padding-right": "10px",
    },
    "span": {
        "border-radius": "0.5rem",
        "color": "rgb(255, 255, 255)",
        "margin": "0 0.125rem",
        "padding": "0.4375rem 0.625rem",
    },
    "active": {
        "background-color": "rgba(255, 255, 255, 0.25)",
    },
    "hover": {
        "background-color": "rgba(255, 255, 255, 0.35)",
    },
}

page = st_navbar(
    pages,
    urls=urls,
    styles=styles,
    options={"show_menu": True, "use_padding": True,}
)
st.write(page)


with st.sidebar:
    st.image(logos, width=70)
    st.write(setting_pr["sidebar_script"])
st.title("UOK 성향 추론 챗봇")
st.write("챗봇과의 대화를 통해 사용자의 성향을 파악할 수 있습니다. 지금 바로 대화를 나눠보세요!")


client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = setting["openai_model"]

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": setting_pr["setting_prompt"]}
    ]

for message in st.session_state.messages[1:]:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.markdown(message["content"])


with st.chat_message("assistant"):
    st.markdown(setting_pr["first_prompt"])

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
