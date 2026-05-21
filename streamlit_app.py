import streamlit as st

st.title("座標の読み取りに関する評価実験")
st.write("Input your informaton!")

student_id = st.text_input("学生番号を入力してください")

field = st.radio(
    "あなたの所属を選んでください",
    ["文系", "理系"]
)


if st.button("次へ"):
    if student_id == "":
        st.warning("学生番号を入力してください。")
    else:
        st.success("入力が完了しました。")
        st.write("番号：", student_id)
        st.write("所属：", field)
        st.write("次の画面からは座標を表示していきます。")
