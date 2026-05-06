import streamlit as st
import requests

# -----------------------------
# Title
# -----------------------------
st.title("総務問い合わせシステム")

# -----------------------------
# Input
# -----------------------------
name = st.text_input("氏名")
question = st.text_area("問い合わせ内容", height=150)

# -----------------------------
# Button
# -----------------------------
if st.button("送信"):

    if question.strip() == "":
        st.error("問い合わせ内容を入力してください。")

    else:
        try:
            # API call
            response = requests.post(
                "http://127.0.0.1:8001/analyze",
                json={"question": question},
                timeout=10
            )

            result = response.json()

            # Show result
            st.subheader("結果")
            st.write("👤 名前:", name)
            st.write("📂 カテゴリ:", result["category"])
            st.write("⚡ 緊急度:", result["priority"])
            st.write("📝 回答:", result["answer"])

            st.success("送信成功！")
            st.balloons()

        except requests.exceptions.ConnectionError:
            st.error("❌ FastAPIが起動していません (backend runしてください)")

        except Exception as e:
            st.error(f"❌ エラー: {e}")