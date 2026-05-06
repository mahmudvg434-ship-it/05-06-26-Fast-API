import streamlit as st
import requests
import pandas as pd
import google.generativeai as genai

# -----------------------------
# Gemini API (নিজের API key বসাও)
# -----------------------------
genai.configure(api_key="YOUR_GEMINI_API_KEY")
model = genai.GenerativeModel("gemini-1.5-flash")

def get_ai_answer(q):
    try:
        response = model.generate_content(q)
        return response.text
    except:
        return "AI error"

# -----------------------------
# CSV file
# -----------------------------
CSV_FILE = "data.csv"

# -----------------------------
# Sidebar menu
# -----------------------------
st.sidebar.title("Menu")
page = st.sidebar.radio("Select", ["📝 Inquiry", "📊 Dashboard"])

# =============================
# 📝 Inquiry Page
# =============================
if page == "📝 Inquiry":

    st.title("総務問い合わせシステム")

    name = st.text_input("氏名")
    question = st.text_area("問い合わせ内容")

    if st.button("送信"):

        if question.strip() == "":
            st.error("内容を入力してください")

        else:
            # API call
            res = requests.post(
                "http://127.0.0.1:8001/analyze",
                json={"question": question}
            )

            result = res.json()

            # show API result
            st.write("カテゴリ:", result["category"])
            st.write("緊急度:", result["priority"])

            # AI answer
            with st.spinner("AI thinking..."):
                ai = get_ai_answer(question)

            st.write("🤖 AI:", ai)

            # save CSV
            df = pd.DataFrame([{
                "name": name,
                "question": question,
                "category": result["category"],
                "priority": result["priority"],
                "ai": ai
            }])

            df.to_csv(CSV_FILE, mode="a", header=False, index=False)

            st.success("Saved!")
            st.balloons()

# =============================
# 📊 Dashboard Page
# =============================
else:

    st.title("Admin Dashboard")

    try:
        df = pd.read_csv(
            CSV_FILE,
            names=["name", "question", "category", "priority", "ai"]
        )

        st.dataframe(df)

    except:
        st.warning("No data yet")