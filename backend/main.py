from fastapi import FastAPI
from pydantic import BaseModel
import google.generativeai as genai
import os
from dotenv import load_dotenv

# -----------------------------
# LOAD GEMINI KEY
# -----------------------------
load_dotenv()
genai.configure(API_KEY ="AIzaSyCBKKEM941MKtv8Gi_EcJS3EEjK4X7iNfc")

model = genai.GenerativeModel("gemini-2.5-flash")

app = FastAPI()

# -----------------------------
# REQUEST MODEL
# -----------------------------
class InquiryRequest(BaseModel):
    question: str

# -----------------------------
# ROOT CHECK
# -----------------------------
@app.get("/")
def root():
    return {"message": "API is running"}

# -----------------------------
# MAIN AI ENDPOINT
# -----------------------------
@app.post("/analyze")
def analyze_inquiry(request: InquiryRequest):

    prompt = f"""
あなたは会社の総務部のAIアシスタントです。

ユーザーの問い合わせ内容:
{request.question}

【重要ルール】
- ユーザーの入力が英語の場合は必ず：
「申し訳ありませんが、日本語のみで入力してください。」
と返すこと

- 日本語のみで丁寧に回答すること
- カテゴリ・緊急度・回答を必ず含めること

【カテゴリ例】
給与、休暇、人事、ITサポート、経費、その他

【緊急度】
低、中、高、緊急

【出力形式（必ずJSONのみ）】
{{
  "category": "",
  "priority": "",
  "answer": ""
}}
"""

    try:
        response = model.generate_content(prompt)
        text = response.text

        # Gemini sometimes adds ```json, so clean it
        text = text.replace("```json", "").replace("```", "")

        import json
        result = json.loads(text)

        return result

    except Exception as e:
        return {
            "category": "その他",
            "priority": "低",
            "answer": f"AI error: {str(e)}"
        }