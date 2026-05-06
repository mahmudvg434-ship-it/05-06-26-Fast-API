import os
from dotenv import load_dotenv
import google.generativeai as genai

import streamlit as st
import requests
import time

# -----------------------------
# LOAD GEMINI
# -----------------------------
load_dotenv()

API_KEY ="AIzaSyCBKKEM941MKtv8Gi_EcJS3EEjK4X7iNfc"

if not API_KEY:
    st.error("❌ GEMINI_API_KEY missing in .env file")

genai.configure(api_key=API_KEY)

model = genai.GenerativeModel("gemini-2.5-flash")

# -----------------------------
# AI FUNCTION
# -----------------------------
def get_ai_answer(text):
    try:
        response = model.generate_content(text)
        return response.text
    except Exception as e:
        return f"AI Error: {e}"

# -----------------------------
# UI
# -----------------------------
st.set_page_config(page_title="総務問い合わせシステム")

st.title("📩 総務問い合わせシステム")

question = st.text_area("📝 問い合わせ内容", height=150)
name = st.text_input("👤 氏名")
email = st.text_input("📧 Email")

# -----------------------------
# BUTTON 1 (MAIN FLOW)
# -----------------------------
if st.button("🚀 API送信"):

    if question.strip() == "":
        st.error("問い合わせ内容を入力してください。")

    else:
        try:
            with st.spinner("処理中...少々お待ちください"):
                time.sleep(1)

                # -----------------------------
                # FASTAPI CALL
                # -----------------------------
                response = requests.post(
                    "http://127.0.0.1:8001/analyze",
                    json={
                        "name": name,
                        "question": question
                    },
                    timeout=10
                )

                if response.status_code != 200:
                    st.error("❌ FastAPI Error")
                    st.stop()

                result = response.json()

                # -----------------------------
                # GEMINI AI CALL
                # -----------------------------
                ai_answer = get_ai_answer(question)

            # -----------------------------
            # RESULT UI (CLEAN CARD)
            # -----------------------------
            st.markdown("## 📦 結果")

            st.markdown(f"""
            <div style="
                background:#f9f9f9;
                padding:20px;
                border-radius:12px;
                border-left:6px solid #4CAF50;
                box-shadow:2px 2px 12px rgba(0,0,0,0.1);
            ">
                <p>👤 <b>名前:</b> {name}</p>
                <p>📧 <b>Email:</b> {email}</p>
                <hr>
                <p>📂 <b>カテゴリ:</b> {result['category']}</p>
                <p>⚡ <b>緊急度:</b> {result['priority']}</p>
                <p>📝 <b>回答:</b> {result['answer']}</p>
                <hr>
                <p>🤖 <b>AI:</b> {ai_answer}</p>
            </div>
            """, unsafe_allow_html=True)

            st.success("✅ 送信成功！")
            st.balloons()

        except requests.exceptions.ConnectionError:
            st.error("❌ FastAPIが起動していません")

        except Exception as e:
            st.error(f"❌ エラー: {e}")