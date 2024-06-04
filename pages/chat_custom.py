import streamlit as st
from openai import OpenAI
from streamlit_navigation_bar import st_navbar
from utils.chat_background import chat_background
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

# page = st_navbar(
#     pages,
#     urls=urls,
#     styles=styles,
#     options={"show_menu": True, "use_padding": True,}
# )
# st.write(page)

with st.sidebar:
    st.image(logos, width=70)
    st.write("Some sidebar content")

# 사용자 정의 CSS 적용
st.markdown(
    """
    <style>
    .user-message, .assistant-message {
        display: flex;
        align-items: center;
        max-width: 60%;
        padding: 15px;
        border-radius: 15px;
        margin: 10px;
        position: relative;
        color: black; /* 글씨 색상 변경 */
    }

    .user-message {
        background-color: rgba(42, 62, 170, 0.5);
        align-self: flex-end;
        margin-left: auto; /* 오른쪽 정렬 */
    }

    .user-message::after {
        content: "";
        position: absolute;
        top: 50%;
        right: -10px;
        transform: translateY(-50%);
        width: 0;
        height: 0;
        border: 10px solid transparent;
        border-left-color: rgba(42, 62, 170, 0.5);
        border-right: 0;
        border-bottom: 0;
        pointer-events: none;
    }

    .assistant-message {
        background-color: rgba(190, 193, 207, 0.2);
        align-self: flex-start;
    }

    .assistant-message::before {
        content: "";
        position: absolute;
        top: 50%;
        left: -10px;
        transform: translateY(-50%);
        width: 0;
        height: 0;
        border: 10px solid transparent;
        border-right-color: rgba(190, 193, 207, 0.2);
        border-left: 0;
        border-top: 0;
        pointer-events: none;
    }

    .message-content {
        margin-left: 10px;
    }

    .stTextInput > div > input:focus {
        border-color: #0073e6; /* 원하는 색상으로 변경 */
        box-shadow: 0 0 0 0.2rem rgba(0, 115, 230, 0.25); /* 원하는 색상으로 변경 */
    }

    .stTextInput > div > input:hover {
        border-color: #0073e6; /* 원하는 색상으로 변경 */
    }

    .main-container {
        background: linear-gradient(to bottom, #ffffff, #d0e4f7);
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.1);
        font-family: "SejonghospitalBold", sans-serif;
        text-align: center;
    }
    </style>
    """,
    unsafe_allow_html=True
)

chat_background()

st.title("UOK 성향 추론 챗봇")
st.write("챗봇과의 대화를 통해 사용자의 성향을 파악할 수 있습니다. 지금 바로 대화를 나눠보세요!")

client = OpenAI(api_key="YOUR_OPENAI_API_KEY")

if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-3.5-turbo"

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "Welcome to the UOK chatbot. How can I help you today?"}
    ]

for message in st.session_state.messages[1:]:
    if message["role"] == "user":
        st.markdown(f'<div class="user-message"><div class="message-content">{message["content"]}</div></div>', unsafe_allow_html=True)
    elif message["role"] == "assistant":
        st.markdown(f'<div class="assistant-message"><div class="message-content">{message["content"]}</div></div>', unsafe_allow_html=True)

st.markdown(
    """
    <div class="assistant-message">
        <div class="message-content">Hello! How can I assist you today?</div>
    </div>
    """,
    unsafe_allow_html=True
)

if prompt := st.chat_input("답변을 작성해주세요 !"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.markdown(f'<div class="user-message"><div class="message-content">{prompt}</div></div>', unsafe_allow_html=True)

    # 실제 OpenAI API 호출을 대신하여 응답 생성 (여기서는 예시 응답)
    response = "This is a placeholder response."  # Replace with your actual API call
    st.markdown(f'<div class="assistant-message"><div class="message-content">{response}</div></div>', unsafe_allow_html=True)
    st.session_state.messages.append({"role": "assistant", "content": response})

st.markdown('</div>', unsafe_allow_html=True)  # chatbox
st.markdown('</div>', unsafe_allow_html=True)  # main-container
