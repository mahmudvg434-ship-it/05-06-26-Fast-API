from fastapi import FastAPI
from pydantic import BaseModel
from backend.storage import save_inquiry, load_inquiries
from datetime import datetime

app = FastAPI()


# =========================
# REQUEST MODEL
# =========================
class InquiryRequest(BaseModel):
    name: str | None = None
    email: str | None = None
    category: str | None = None
    question: str


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

    text = request.question.lower()
    category = request.category or "その他"

    # =========================
    # DEFAULT VALUES
    # =========================
    department = "総務部"
    priority = "低"

    # =========================
    # LOGIC
    # =========================
    if category == "給与" or "salary" in text or "給料" in text:
        department = "人事・経理部"
        priority = "高"
        answer = "給与に関するお問い合わせを受け付けました。"

    elif category == "休暇" or "leave" in text or "休暇" in text:
        department = "総務部"
        priority = "中"
        answer = "休暇申請に関するお問い合わせを受け付けました。"

    elif category == "福利厚生":
        department = "総務部"
        priority = "中"
        answer = "福利厚生に関するお問い合わせを受け付けました。"

    else:
        department = "総務部"
        priority = "低"
        answer = "お問い合わせ内容を受け付けました。"

    # =========================
    # JAPANESE COMPANY MESSAGE (YOU ASKED THIS PART)
    # =========================
    answer += """

現在、人事・経理部にて内容を確認しております。
確認完了後、担当者よりご連絡いたしますので、
今しばらくお待ちください。
"""

    # =========================
    # SAVE HISTORY
    # =========================
    item = save_inquiry(
        name=request.name,
        email=request.email,
        question=request.question,
        category=category,
        priority=priority,
        department=department,
        status="未対応",
        answer=answer,
    )

    return item


# =========================
# HISTORY API
# =========================
@app.get("/inquiries")
def get_inquiries():
    return load_inquiries()