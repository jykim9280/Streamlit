import json
from dotenv import load_dotenv
import google.generativeai as genai
import os

# .env 파일에서 환경 변수 로드
load_dotenv()  # 반드시 os.environ에서 API_KEY를 불러오기 전에 호출해야 합니다.

# 환경 변수에서 API 키 가져오기
api_key = os.getenv("API_KEY")
if api_key:
    genai.configure(api_key=api_key)
else:
    print("API_KEY가 설정되지 않았습니다.")
    exit()  # API 키가 없을 경우 프로그램 종료

# 데이터 로드
with open(r'C:\Users\5-12\Downloads\Sample\Sample\02.라벨링데이터\국정감사\16\LAB_16대_2000_2000년10월20일_국정감사_교육위원회_0001(030043).json', 'r', encoding='utf-8') as file:
    data = json.load(file)

# 질문-답변 추출
qa_pairs = []
qa_pairs.append({
    'question': data['question']['comment'], 
    'answer': data['answer']['comment']
})

# Gemini 모델 초기화
model = genai.GenerativeModel("gemini-1.5-flash")
chat = model.start_chat()

# 질문에 대한 답변 생성
def LLM_Response(question):
    response = chat.send_message(question)
    # 응답 객체에서 텍스트 추출
    if response.candidates:
        return response.candidates[0].content.parts[0].text
    else:
        return "응답을 생성할 수 없습니다."

# 데이터에서 관련 질문 검색
def get_answer(question):
    for pair in qa_pairs:
        if pair['question'] in question:
            return pair['answer']
    return LLM_Response(question)

# 테스트
user_question = "신도시 평준화 정책에 대해 알려주세요."
answer = get_answer(user_question)
print(answer)