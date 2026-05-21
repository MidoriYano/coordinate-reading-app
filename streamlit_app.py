import streamlit as st
from datetime import datetime

st.title("座標の読み取りに関する評価実験")

images = [
    "https://placehold.co/600x400?text=Image+1",
    "https://placehold.co/600x400?text=Image+2",
    "images/image3.png",
    # "https://placehold.co/600x400?text=Image+3",
]

if "page" not in st.session_state:
    st.session_state.page = "start"

if "image_index" not in st.session_state:
    st.session_state.image_index = 0

if "answers" not in st.session_state:
    st.session_state.answers = []

if "image_start_time" not in st.session_state:
    st.session_state.image_start_time = None

# -------------------------
# 最初の画面
# -------------------------

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
        st.session_state.image_start_time = datetime.now()
        st.rerun()

# -------------------------
# 画像回答画面
# -------------------------
elif st.session_state.page == "image":
    # st.write("画像を見て座標を回答してください。")
    # st.image("https://placehold.co/600x400?text=Sample+Image")

    index = st.session_state.image_index

    st.write(f"画像 {index + 1} / {len(images)}")
    st.image(images[index])

    answer = st.text_area("画像を見て座標を回答してください。")

    if st.button("次の画像へ"):

        button_time = datetime.now()

        st.session_state.answers.append({
            "image": index + 1,
            "answer": answer
            "image_start_time": st.session_state.image_start_time,
            "button_time": button_time,
            "display_seconds": (button_time - st.session_state.image_start_time).total_seconds()
        })
        
        if index < len(images) - 1:
            st.session_state.image_index += 1
            st.session_state.image_start_time = datetime.now()
            st.rerun()
        else:
            st.session_state.page = "end"
            st.rerun()
        # st.success("次の画像に進む予定です。")
        # st.write("学生番号：", st.session_state.student_id)
        # st.write("所属：", st.session_state.field)
        # st.write("回答：", answer)

# -------------------------
# 終了画面
# -------------------------
elif st.session_state.page == "end":
    st.success("終了です。ご協力いただきありがとうございました。")

    st.write("学生番号：", st.session_state.student_id)
    st.write("所属：", st.session_state.field)
    
    st.write("### 回答一覧")

    for item in st.session_state.answers:
        st.write(f"画像 {item['image']}")
        st.write("回答：", item["answer"])
        st.write("表示開始時刻：", item["image_start_time"])
        st.write("ボタン押下時刻：", item["button_time"])
        st.write("表示時間（秒）：", item["display_seconds"])
        st.write("---")
