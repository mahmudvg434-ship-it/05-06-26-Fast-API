else:

    import time

    try:
        # ⏳ loading effect (এখানে বসবে)
        with st.spinner("処理中...少々お待ちください"):
            time.sleep(2)

            # API call
            response = requests.post(
                "http://127.0.0.1:8001/analyze",
                json={"question": question},
                timeout=10
            )

            result = response.json()

        # Show result (spinner শেষ হওয়ার পরে)
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