import streamlit as st
from openai import OpenAI
import toml


client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
prompts = toml.load('static/toml/prompts.toml')

def generate_result(target_name, result):
    messages=[]
    messages.append({
        "role": "system", "content": prompts["result_prompt"]
    })
    # result 값들 넣어주기, 아래 코드 참고
    # messages=[ 
    #     {"role": m["role"], "content": m["content"]}
    #     for m in st.session_state.messages
    # ].copy()

    response = client.chat.completions.create(
        model=st.session_state["openai_model"],
        max_tokens=1000,
        temperature = 1, 
        presence_penalty= 1.7,
        messages=messages
    )
    return response.choices[0].message.content