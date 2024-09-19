# main.py
import os
import streamlit as st
from dotenv import load_dotenv
import google.generativeai as genai

# .env 파일에서 환경 변수 로드
load_dotenv()  # 반드시 os.environ에서 API_KEY를 불러오기 전에 호출해야 합니다.

safety_settings=[
        {
            "category": "HARM_CATEGORY_HARASSMENT",
            "threshold": "BLOCK_NONE",
        },
        {
            "category": "HARM_CATEGORY_HATE_SPEECH",
            "threshold": "BLOCK_NONE",
        },
    ]


# 환경 변수에서 API 키 가져오기
api_key = os.getenv("API_KEY")
if api_key:
    genai.configure(api_key=api_key)
else:
    print("API_KEY가 설정되지 않았습니다.")

model = genai.GenerativeModel("gemini-1.5-flash", safety_settings)
chat = model.start_chat()

def LLM_Response(question):
    response = chat.send_message(question,stream=True)
    return response

st.title("Chat Application using Gemini Pro")

user_quest = st.text_input("Ask a question:")
btn = st.button("Ask")

if btn and user_quest:
    result = LLM_Response(user_quest)
    st.subheader("Response : ")
    for word in result:
        st.text(word.text)