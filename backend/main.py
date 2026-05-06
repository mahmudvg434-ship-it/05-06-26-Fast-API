from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class InquiryRequest(BaseModel):
    question: str

@app.get("/")
def root():
    return {"message": "API is running"}

@app.post("/analyze")
def analyze(req: InquiryRequest):

    q = req.question.lower()

    if "salary" in q:
        category = "給与"
        priority = "高"
        answer = "給与の問い合わせです"
    elif "leave" in q:
        category = "休暇"
        priority = "中"
        answer = "休暇の問い合わせです"
    else:
        category = "その他"
        priority = "低"
        answer = "問い合わせを受け付けました"

    return {
        "category": category,
        "priority": priority,
        "answer": answer
    }