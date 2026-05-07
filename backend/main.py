from fastapi import FastAPI
from pydantic import BaseModel
from backend.storage import save_inquiry, load_inquiries

import os
from dotenv import load_dotenv
from google import genai

# =========================
# LOAD ENV
# =========================
load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")
MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")

app = FastAPI()

# =========================
# SAFE GEMINI CLIENT INIT
# =========================
client = None

if not API_KEY:
    print("❌ GEMINI_API_KEY not found in .env file")
else:
    try:
        client = genai.Client(api_key=API_KEY)
        print("✅ Gemini Client Initialized")
    except Exception as e:
        print("❌ Gemini init failed:", e)


# =========================
# REQUEST MODEL
# =========================
class InquiryRequest(BaseModel):
    name: str | None = None
    email: str | None = None
    category: str | None = None
    question: str


# =========================
# GEMINI FUNCTION
# =========================
def analyze_with_gemini(question: str):

    if client is None:
        return "AIシステムは現在利用できません。（API設定を確認してください）"

    prompt = f"""
あなたは会社の総務AIです。

以下の形式で回答してください：
1. カテゴリ
2. 緊急度（高・中・低）
3. 回答案

問い合わせ:
{question}
"""

    try:
        response = client.models.generate_content(
            model=MODEL,
            contents=prompt
        )

        return response.text

    except Exception as e:
        print("❌ Gemini Error:", e)
        return "AIシステムでエラーが発生しましたが、問い合わせは受け付けました。"


# =========================
# ROOT
# =========================
@app.get("/")
def root():
    return {"message": "API is running"}


# =========================
# ANALYZE API
# =========================
@app.post("/analyze")
def analyze_inquiry(request: InquiryRequest):

    ai_result = analyze_with_gemini(request.question)

    item = save_inquiry(
        name=request.name,
        email=request.email,
        question=request.question,
        category=request.category or "その他",
        priority="AI判断",
        department="AIシステム",
        status="未対応",
        answer=ai_result
    )

    return item


# =========================
# HISTORY API
# =========================
@app.get("/inquiries")
def get_inquiries():
    return load_inquiries()