import streamlit as st

def main_background():
    main_background = '''
    <style>
    .stApp {
    background-size: cover;
    background: linear-gradient(to bottom, #ffffff, #AFD8FF);
    }
    </style>
    '''
    st.markdown(main_background, unsafe_allow_html=True)