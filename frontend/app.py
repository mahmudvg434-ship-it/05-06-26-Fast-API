import streamlit as st
import requests

st.set_page_config(page_title="総務問い合わせシステム", layout="centered")

# =========================
# SIDEBAR MENU
# =========================
menu = st.sidebar.selectbox(
    "メニュー",
    ["総務問い合わせ入力", "履歴"]
)

# =========================
# API BASE URL
# =========================
API_URL = "http://127.0.0.1:8001"


# =========================
# PAGE 1 - INPUT
# =========================
if menu == "総務問い合わせ入力":

    st.title("📩 会社用 AI 問い合わせシステム")

    name = st.text_input("👤 氏名")
    email = st.text_input("📧 Email")

    category = st.selectbox(
        "カテゴリ",
        ["休暇", "給与", "福利厚生", "その他"]
    )

    question = st.text_area("📝 問い合わせ内容", height=180)

    if st.button("API 送信する"):

        if question.strip() == "":
            st.error("問い合わせ内容を入力してください。")
            st.stop()

        try:
            with st.spinner("処理中..."):

                response = requests.post(
                    f"{API_URL}/analyze",
                    json={
                        "name": name,
                        "email": email,
                        "category": category,   # ✅ FIXED
                        "question": question
                    },
                    timeout=30
                )

                if response.status_code != 200:
                    st.error("API エラーが発生しました")
                    st.stop()

                result = response.json()

            st.success("送信完了 🎉")

            # =========================
            # RESULT CARD
            # =========================
            st.markdown("## 📦 結果")

            st.markdown(f"""
            <div style="
                background:#f9f9f9;
                padding:20px;
                border-radius:12px;
                border-left:6px solid #4CAF50;
                box-shadow:2px 2px 12px rgba(0,0,0,0.1);
            ">
                <p>👤 <b>名前:</b> {result.get('name', '')}</p>
                <p>📧 <b>Email:</b> {result.get('email', '')}</p>
                <p>📂 <b>カテゴリ:</b> {result.get('category', '')}</p>
                <p>🏢 <b>部署:</b> {result.get('department', '')}</p>
                <p>⚡ <b>緊急度:</b> {result.get('priority', '')}</p>
                <p>📌 <b>ステータス:</b> {result.get('status', '')}</p>
                <hr>
                <p>🤖 <b>回答:</b><br>{result.get('answer', '')}</p>
            </div>
            """, unsafe_allow_html=True)

        except Exception as e:
            st.error(f"❌ 接続エラー: {e}")


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
            st.stop()

        for item in reversed(inquiries):

            st.markdown("---")

            st.markdown(f"""
            ### 🆔 ID: {item.get('id', '')}

            📅 **日時:** {item.get('created_at', '')}  
            👤 **名前:** {item.get('name', '')}  
            📧 **Email:** {item.get('email', '')}  

            📝 **内容:** {item.get('question', '')}  
            📂 **カテゴリ:** {item.get('category', '')}  
            🏢 **部署:** {item.get('department', '')}  
            ⚡ **緊急度:** {item.get('priority', '')}  
            📌 **ステータス:** {item.get('status', '')}  

            🤖 **回答:**  
            {item.get('answer', '')}
            """)

    except Exception as e:
        st.error(f"❌ API接続エラー: {e}")