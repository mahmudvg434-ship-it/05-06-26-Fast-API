from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class InquiryRequest(BaseModel):
    question: str

@app.get("/")
def root():
    return {"message": "API is running"}

@app.post("/analyze")
def analyze_inquiry(request: InquiryRequest):

    q = request.question.lower()

    if "salary" in q:
        category = "給与"
        priority = "高"
    elif "leave" in q:
        category = "休暇"
        priority = "中"
    else:
        category = "その他"
        priority = "低"

    return {
        "category": category,
        "priority": priority,
        "answer": f"問い合わせを受け付けました: {request.question}"
    }