import streamlit as st
import requests
import time

# -----------------------------
# Title
# -----------------------------
st.title("総務問い合わせシステム")

# -----------------------------
# Input
# -----------------------------
name = st.text_input("👤 氏名")
email = st.text_input("📧 Email")
question = st.text_area("📝 問い合わせ内容", height=150)

# -----------------------------
# Button
# -----------------------------
if st.button("送信"):

    if question.strip() == "":
        st.error("問い合わせ内容を入力してください。")

    else:
        try:
            # ⏳ loading effect
            with st.spinner("処理中...少々お待ちください"):
                time.sleep(2)

                # API call
                response = requests.post(
                    "http://127.0.0.1:8001/analyze",
                    json={
                        "name": name,
                        "question": question
                    },
                    timeout=10
                )

                result = response.json()

            # -----------------------------
            # BEAUTIFUL RESULT CARD
            # -----------------------------
            st.markdown("## 📦 結果")

            st.markdown(f"""
            <div style="
                background-color:#f9f9f9;
                padding:20px;
                border-radius:12px;
                border-left:6px solid #4CAF50;
                box-shadow:2px 2px 12px rgba(0,0,0,0.1);
                margin-bottom:10px;
            ">
                <p>👤 <b>名前:</b> {name}</p>
                <p>📧 <b>Email:</b> {email}</p>
                <p>📂 <b>カテゴリ:</b> {result['category']}</p>
                <p>⚡ <b>緊急度:</b> {result['priority']}</p>
                <p>📝 <b>回答:</b> {result['answer']}</p>
            </div>
            """, unsafe_allow_html=True)

            st.success("✅ 送信成功！")
            st.balloons()

        except requests.exceptions.ConnectionError:
            st.error("❌ FastAPIが起動していません")

        except Exception as e:
            st.error(f"❌ エラー: {e}")