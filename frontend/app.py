import streamlit as st
import requests

st.title("総務問い合わせシステム")

question = st.text_area("問い合わせ内容")

if st.button("送信"):

    response = requests.post(
        "http://127.0.0.1:8001/analyze",
        json={"question": question}
    )

    result = response.json()

    st.write("カテゴリ:", result["category"])
    st.write("緊急度:", result["priority"])
    st.write("回答:", result["answer"])

    st.balloons()