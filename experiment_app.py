import streamlit as st
from datetime import datetime
# import csv
# import os
import gspread
from google.oauth2.service_account import Credentials

st.title("座標の読み取りに関する評価実験")

images = [
    "https://placehold.co/600x400?text=Image+1",
    "https://placehold.co/600x400?text=Image+2",
    "images/image3.png",
    # "https://placehold.co/600x400?text=Image+3",
]

# csv_file = "answer.csv"

# -------------------------
# Gスプレッドシート書き込み準備
# -------------------------
scope = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

credentials = Credentials.from_service_account_info(
    st.secrets,
    scopes=scope
)

client = gspread.authorize(credentials)
# sheet = client.open(st.secrets["spreadsheet_name"]).sheet1
sheet = client.open_by_key(
    st.secrets["spreadsheet_id"]
).sheet1

# -------------------------
# 初期設定
# -------------------------

if "page" not in st.session_state:
    st.session_state.page = "start"

if "image_index" not in st.session_state:
    st.session_state.image_index = 0

if "answers" not in st.session_state:
    st.session_state.answers = []

if "image_start_time" not in st.session_state:
    st.session_state.image_start_time = None

if "submitted" not in st.session_state:
    st.session_state.submitted = False

# -------------------------
# 回答保存
# -------------------------

# def save_to_csv():
#     file_exists = os.path.exists(csv_file)

#     with open(csv_file, "a", newline="", encoding="utf-8-sig") as f:
#         writer = csv.writer(f)

#         if not file_exists:
#             writer.writerow([
#                 "学生番号",
#                 "文理選択",
#                 "画像番号",
#                 "回答",
#                 "表示開始時刻",
#                 "ボタン押下時刻",
#                 "表示時間_秒"
#             ])

#         for item in st.session_state.answers:
#             writer.writerow([
#                 st.session_state.student_id,
#                 st.session_state.field,
#                 item["image"],
#                 item["answer"],
#                 item["image_start_time"],
#                 item["button_time"],
#                 item["display_seconds"]
#             ])

def save_to_google_sheets():
    for item in st.session_state.answers:
        sheet.append_row([
            st.session_state.student_id,
            st.session_state.field,
            item["image"],
            item["answer"],
            str(item["image_start_time"]),
            str(item["button_time"]),
            item["display_seconds"]
        ])


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
            # st.write("文理選択：", field)
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

    # answer = st.text_area("画像を見て座標を回答してください。")
    answer = st.text_area(
    "画像を見て座標を回答してください。",
    key=f"answer_{index}"
    )

    # if st.button("次の画像へ"):
    if st.button("次の画像へ", disabled=st.session_state.submitted):

        # 回答空欄チェック
        if answer.strip() == "":
            st.warning("回答を入力してください。")
            st.stop()

        # 二重送信防止
        st.session_state.submitted = True
            
        button_time = datetime.now()

        st.session_state.answers.append({
            "image": index + 1,
            "answer": answer,
            "image_start_time": st.session_state.image_start_time,
            "button_time": button_time,
            "display_seconds": (button_time - st.session_state.image_start_time).total_seconds()
        })
        
        if index < len(images) - 1:
            st.session_state.image_index += 1
            st.session_state.image_start_time = datetime.now()
            st.session_state.submitted = False
            st.rerun()
        else:
            save_to_google_sheets()
            st.session_state.page = "end"
            st.session_state.submitted = False
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
    # st.write("回答はCSVに保存されました。")
    st.write("回答はGoogleスプレッドシートに保存されました。")

    st.write("学生番号：", st.session_state.student_id)
    st.write("文理選択：", st.session_state.field)
    
    st.write("### 回答一覧")

    for item in st.session_state.answers:
        st.write(f"画像 {item['image']}")
        st.write("回答：", item["answer"])
        # st.write("表示開始時刻：", item["image_start_time"])
        # st.write("ボタン押下時刻：", item["button_time"])
        st.write("表示時間（秒）：", item["display_seconds"])
        st.write("---")
