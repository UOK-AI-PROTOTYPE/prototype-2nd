import streamlit as st
from utils.main_background import main_background
from utils.modal import trigger1
from intro import set_intro
from description import set_description
import streamlit.components.v1 as components
import toml, json

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


# st.markdown("src/image/main_image.png", unsafe_allow_html=True)

if st.button("지금 바로 분석하기"):
    trigger1()
    # enter_modal()