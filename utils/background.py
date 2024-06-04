import streamlit as st

def set_background():
    background = '''
    <style>
    .stApp {
    background-size: cover;
    background: linear-gradient(to bottom, #ffffff, #AFD8FF);
    }
    </style>
    '''
    st.markdown(background, unsafe_allow_html=True)