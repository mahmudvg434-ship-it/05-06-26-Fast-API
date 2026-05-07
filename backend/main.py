from fastapi import FastAPI
from pydantic import BaseModel
from backend.storage import save_inquiry, load_inquiries

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

    # =========================
    # DEFAULT VALUES
    # =========================
    category = request.category or "その他"
    department = "総務部"
    priority = "低"
    answer = ""

    # =========================
    # LOGIC ENGINE
    # =========================
    if "salary" in text or "給料" in text or "pay" in text:
        category = "給与"
        department = "人事・経理部"
        priority = "高"
        answer = "給与に関するお問い合わせを受け付けました。"

    elif "leave" in text or "休暇" in text or "vacation" in text:
        category = "休暇"
        department = "総務部"
        priority = "中"
        answer = "休暇申請に関するお問い合わせを受け付けました。"

    elif "benefit" in text or "福利厚生" in text:
        category = "福利厚生"
        department = "総務部"
        priority = "中"
        answer = "福利厚生に関するお問い合わせを受け付けました。"

    else:
        answer = "お問い合わせ内容を受け付けました。"

    # =========================
    # DYNAMIC JAPANESE MESSAGE (FIXED)
    # =========================
    if department == "人事・経理部":
        answer += """

現在、人事・経理部にて内容を確認しております。
"""

    else:
        answer += f"""

現在、{department}にて内容を確認しております。
"""

    answer += """
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