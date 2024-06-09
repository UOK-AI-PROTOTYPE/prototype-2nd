import streamlit as st
from utils.main_background import main_background
from intro import set_intro
from utils.modal import enter_modal
from description import set_description
import toml

setting = toml.load('setting.toml')
prompts = toml.load('prompts.toml')
json_styles = 'styles.json'

st.set_page_config(
    initial_sidebar_state="collapsed",
    page_title="UOK AI PROJECT",
    page_icon=setting["page_icon"],
    layout="centered",
)

main_background()
set_intro()
set_description()

if st.button("지금 바로 분석 하러가기"):
    st.switch_page("pages/chat.py")