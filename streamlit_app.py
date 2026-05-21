import streamlit as st

st.title("座標の読み取りに関する評価実験")

if "page" not in st.session_state:
    st.session_state.page = "start"

if st.session_state.page == "start":
    st.write("Input your informaton!")

student_id = st.text_input("学生番号を入力してください")

field = st.radio(
    "自分の専攻にもとづいて選択してください",
    ["文系", "理系", "わからない"]
)


if st.button("次へ"):
    if student_id == "":
        st.warning("学生番号を入力してください。")
    else:
        # st.success("入力が完了しました。")
        # st.write("学生番号：", student_id)
        # st.write("専攻：", field)
        # st.write("次の画面からは座標を表示していきます。")
        st.session_state.student_id = student_id
        st.session_state.field = field
        st.session_state.page = "image"
        st.rerun()

elif st.session_state.page == "image":
    st.write("画像を見て座標を回答してください。")

    st.image("https://placehold.co/600x400?text=Sample+Image")

    answer = st.text_area("画像を見て座標を回答してください。")

    if st.button("次の画像へ"):
        st.success("次の画像に進む予定です。")
        st.write("番号：", st.session_state.student_id)
        st.write("所属：", st.session_state.field)
        st.write("回答：", answer)
