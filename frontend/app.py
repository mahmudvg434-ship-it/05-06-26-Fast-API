import streamlit as st
import requests

# =========================
# CONFIG
# =========================
st.set_page_config(page_title="総務問い合わせシステム", layout="centered")

API_URL = "http://127.0.0.1:8001"


# =========================
# MENU
# =========================
menu = st.sidebar.selectbox(
    "メニュー",
    ["総務問い合わせ入力", "履歴"]
)


# =========================
# PAGE 1 - INPUT FORM
# =========================
if menu == "総務問い合わせ入力":

    st.title("📩 会社用 AI 問い合わせシステム")

    name = st.text_input("👤 氏名")
    email = st.text_input("📧 Email")

    category = st.selectbox(
        "📂 カテゴリ",
        ["休暇", "給与", "福利厚生", "その他"]
    )

    question = st.text_area("📝 問い合わせ内容", height=180)

    if st.button("API 送信する"):

        if not question.strip():
            st.error("問い合わせ内容を入力してください。")

        else:
            try:
                with st.spinner("送信中..."):

                    response = requests.post(
                        f"{API_URL}/analyze",
                        json={
                            "name": name,
                            "email": email,
                            "category": category,
                            "question": question
                        },
                        timeout=30
                    )

                if response.status_code != 200:
                    st.error(response.text)
                else:
                    result = response.json()

                    st.success("送信完了 🎉")

                    st.subheader("📦 結果")

                    st.write("👤 名前:", result.get("name", ""))
                    st.write("📧 Email:", result.get("email", ""))
                    st.write("📂 カテゴリ:", result.get("category", ""))
                    st.write("🏢 部署:", result.get("department", ""))
                    st.write("⚡ 緊急度:", result.get("priority", ""))
                    st.write("📌 ステータス:", result.get("status", ""))

                    st.markdown("### 🤖 回答")
                    st.info(result.get("answer", ""))

            except Exception as e:
                st.error(f"エラー: {e}")


# =========================
# PAGE 2 - HISTORY
# =========================
elif menu == "履歴":

    st.title("📚 問い合わせ履歴")

    try:
        resp = requests.get(f"{API_URL}/inquiries", timeout=10)

        if resp.status_code != 200:
            st.error("履歴取得エラー")
            st.stop()

        inquiries = resp.json()

        if not inquiries:
            st.info("履歴がありません")

        else:
            for item in reversed(inquiries):

                st.markdown("---")

                # CARD STYLE BOX
                with st.container():

                    st.subheader(f"🆔 ID: {item.get('id','')}")

                    col1, col2 = st.columns(2)

                    with col1:
                        st.write("📅 日時:", item.get("created_at", ""))
                        st.write("👤 名前:", item.get("name", ""))
                        st.write("📧 Email:", item.get("email", ""))
                        st.write("📂 カテゴリ:", item.get("category", ""))

                    with col2:
                        st.write("🏢 部署:", item.get("department", ""))
                        st.write("⚡ 緊急度:", item.get("priority", ""))
                        st.write("📌 ステータス:", item.get("status", ""))

                    st.write("📝 内容:")
                    st.write(item.get("question", ""))

                    st.markdown("### 🤖 回答")
                    st.success(item.get("answer", ""))

    except Exception as e:
        st.error(f"エラー: {e}")