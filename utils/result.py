import streamlit as st
from openai import OpenAI
import toml


client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
prompts = toml.load('static/toml/prompts.toml')

def generate_result():
    # target_name = st.session_state.user_info[1]
    target_name = st.session_state['target_name']
    # system 메세지
    messages = [{
        "role": "system", "content": f"""target_name : {target_name}, prompt: {prompts["result_prompt"]}"""
    }]

    # 사용자 메시지를 추가
    messages.extend([{
        "role": "user", "content": f"name: {data['name']}, relation: {data['relation']}, result: {data['result']}"
    } for data in st.session_state.participant])

    response = client.chat.completions.create(
        model=st.session_state["openai_model"],
        max_tokens=1000,
        temperature = 1, 
        presence_penalty= 1.7,
        messages=messages
    )
    return response.choices[0].message.content