import streamlit as st

def chat_background():
    chat_background = '''
    <style>
    .stApp {
    background: linear-gradient(to bottom, #BEDFFF 0%, #BEDFFF 10%,  #ffffff 35%, #ffffff 0%);
    background-size: contain;    
    </style>
    '''
    st.markdown(chat_background, unsafe_allow_html=True)
