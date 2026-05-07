import streamlit as st
import requests

st.set_page_config(page_title="総務問い合わせシステム")

# =========================
# SIDEBAR MENU
# =========================
menu = st.sidebar.selectbox(
    "メニュー",
    ["総務問い合わせ入力", "履歴"]
)

# =========================
# PAGE 1
# =========================
if menu == "総務問い合わせ入力":

    st.title("📩 会社用 AI 問い合わせシステム")

    name = st.text_input("👤 氏名")
    email = st.text_input("📧 Email")

    question = st.text_area(
        "📝 問い合わせ内容",
        height=180
    )

    if st.button("送信する"):

        if question.strip() == "":
            st.error("問い合わせ内容を入力してください。")

        else:

            response = requests.post(
                "http://127.0.0.1:8001/analyze",
                json={
                    "name": name,
                    "email": email,
                    "question": question
                },
                timeout=30
            )

            result = response.json()

            st.success("送信完了")

            st.markdown("## 📦 結果")

            st.write("👤 名前:", result["name"])
            st.write("📧 Email:", result["email"])
            st.write("📂 カテゴリ:", result["category"])
            st.write("🏢 部署:", result["department"])
            st.write("⚡ 緊急度:", result["priority"])
            st.write("📌 ステータス:", result["status"])
            st.write("🤖 回答:", result["answer"])

# =========================
# PAGE 2
# =========================
elif menu == "履歴":

    st.title("📚 問い合わせ履歴")

    resp = requests.get(
        "http://127.0.0.1:8001/inquiries",
        timeout=10
    )

    if resp.status_code == 200:

        inquiries = resp.json()

        if inquiries:

            for item in reversed(inquiries):

                st.markdown("---")

                st.write("🆔 ID:", item["id"])
                st.write("📅 日時:", item["created_at"])
                st.write("👤 名前:", item["name"])
                st.write("📧 Email:", item["email"])
                st.write("📝 内容:", item["question"])
                st.write("📂 カテゴリ:", item["category"])
                st.write("🏢 部署:", item["department"])
                st.write("⚡ 緊急度:", item["priority"])
                st.write("📌 ステータス:", item["status"])
                st.write("🤖 回答:", item["answer"])

        else:
            st.info("履歴がありません")