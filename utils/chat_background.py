import streamlit as st

def chat_background():
    chat_background = '''
    <style>
    .stApp {
    background-size: cover;
    background: linear-gradient(to bottom, #BEDFFF 0%, #BEDFFF 75%, #ffffff 75%, #ffffff 100%);
    </style>
    '''
    st.markdown(chat_background, unsafe_allow_html=True)