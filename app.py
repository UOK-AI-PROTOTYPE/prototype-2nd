import streamlit as st
from utils.main_background import main_background
from main.intro import set_intro
from main.description import set_description
from utils.signIn_modal import signIn_modal
import toml

setting = toml.load('static/toml/setting.toml')
prompts = toml.load('static/toml/prompts.toml')
json_styles = 'staitc/json/styles.json'

st.set_page_config(
    initial_sidebar_state="collapsed",
    page_title="UOK AI PROJECT",
    page_icon=setting["page_icon"],
    layout="centered",
)

main_background()
set_intro()
set_description()

# CSS for alignment
st.markdown("""
    <style>
    div.stButton > button {
        display: block;
        margin: 0 auto;
    }
    </style>
""", unsafe_allow_html=True)

if st.button("지금 바로 분석 하러가기"):
    # signIn_modal()
    st.switch_page("pages/database.py")
