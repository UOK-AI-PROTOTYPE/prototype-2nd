import streamlit as st
from streamlit_navigation_bar import st_navbar
import json

def set_navbar():

    json_styles = 'styles.json'

    pages = ["ChatBot"]
    # urls = {"UOK": "http://localhost:8501/chat"}
    with open(json_styles, 'r') as file:
        styles = json.load(file)

    # CSS로 특정 요소 숨기기
    hide_text_css = """
    <style>
    .stApp p {
        display: none !important;
    }
    </style>
    """

    page = st_navbar(
        pages,
        # urls=urls,
        styles=styles,
        options={"show_menu": True, "use_padding": False,}
    )

    # CSS 추가
    st.markdown(hide_text_css, unsafe_allow_html=True)

    st.write(page)
