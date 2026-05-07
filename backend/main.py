from fastapi import FastAPI
from pydantic import BaseModel
from backend.storage import save_inquiry, load_inquiries

app = FastAPI()

# =========================
# REQUEST MODEL
# =========================
class InquiryRequest(BaseModel):
    name: str
    email: str
    question: str


# =========================
# ROOT API
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

    # -------------------------
    # CATEGORY LOGIC
    # -------------------------
    if "salary" in text or "給料" in text:
        category = "給与"
        department = "人事・経理部"
        priority = "高"

        answer = """
給与に関するお問い合わせを受け付けました。

人事・経理部に内容を共有いたします。
確認後、担当者よりご連絡いたしますので、
しばらくお待ちください。
"""

    elif "leave" in text or "休暇" in text:
        category = "休暇"
        department = "総務部"
        priority = "中"

        answer = """
休暇申請に関するお問い合わせを受け付けました。

申請方法について確認後、
総務部よりご案内いたします。
"""

    elif "pc" in text or "パソコン" in text:
        category = "設備"
        department = "情報システム部"
        priority = "中"

        answer = """
設備に関するお問い合わせを受け付けました。

情報システム部に確認を依頼いたします。
"""

    else:
        category = "その他"
        department = "総務部"
        priority = "低"

        answer = """
お問い合わせ内容を受け付けました。

担当部署に内容を共有し、
順次対応いたします。
"""

    # =========================
    # SAVE JSON HISTORY
    # =========================
    item = save_inquiry(
        name=request.name,
        email=request.email,
        question=request.question,
        category=category,
        priority=priority,
        department=department,
        status="未対応",
        answer=answer
    )

    return item


# =========================
# HISTORY API
# =========================
@app.get("/inquiries")
def get_inquiries():
    return load_inquiries()