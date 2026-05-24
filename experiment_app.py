import streamlit as st
from datetime import datetime
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials

st.title("座標の読み取りに関する評価実験")

# trials_all = pd.read_csv("trials.csv")

# -------------------------
# trials.csv 読み込み
# -------------------------
REQUIRED_COLUMNS = [
    "group",
    "trial_order",
    "series_id",
    "condition",
    "task",
    "image_file",
    "true_answer",
]

trials_all = pd.read_csv("trials.csv", dtype={"true_answer": str})
missing_columns = [col for col in REQUIRED_COLUMNS if col not in trials_all.columns]

if missing_columns:
    st.error(f"trials.csv に必要な列がありません: {missing_columns}")
    st.stop()


# -------------------------
# Gスプレッドシート書き込み準備
# -------------------------
# scope = [
#     "https://www.googleapis.com/auth/spreadsheets",
#     "https://www.googleapis.com/auth/drive"
# ]

# credentials = Credentials.from_service_account_info(
#     st.secrets,
#     scopes=scope
# )

# client = gspread.authorize(credentials)

# sheet = client.open_by_key(
#     st.secrets["spreadsheet_id"]
# ).sheet1

@st.cache_resource
def connect_to_sheet():
    scope = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive"
    ]

    credentials = Credentials.from_service_account_info(
        st.secrets,
        scopes=scope
    )

    client = gspread.authorize(credentials)
    return client.open_by_key(st.secrets["spreadsheet_id"]).sheet1

sheet = connect_to_sheet()

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

if "saved_to_sheet" not in st.session_state:
    st.session_state.saved_to_sheet = False

# -------------------------
# 回答保存
# -------------------------

def save_to_google_sheets():
    # for item in st.session_state.answers:
    #     sheet.append_row([
    #         datetime.now().isoformat(),
    #         item["participant_id"],
    #         item["assigned_group"],
    #         item["trial_order"],
    #         item["series_id"],
    #         item["condition"],
    #         item["task"],
    #         item["image_file"],
    #         item["true_answer"],
    #         item["response"],
    #         item["correct"],
    #         item["abs_error"],
    #         str(item["image_start_time"]),
    #         str(item["button_time"]),
    #         item["display_seconds"]
    #     ])
    if st.session_state.saved_to_sheet:
        return

    rows = []
    for item in st.session_state.answers:
        rows.append([
            datetime.now().isoformat(),
            item["participant_id"],
            item["assigned_group"],
            item["trial_order"],
            item["series_id"],
            item["condition"],
            item["task"],
            item["image_file"],
            item["true_answer"],
            item["response"],
            item["correct"],
            item["abs_error"],
            str(item["image_start_time"]),
            str(item["button_time"]),
            item["display_seconds"]
        ])
        
    sheet.append_rows(rows)
    st.session_state.saved_to_sheet = True
    
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

    assigned_group = st.radio(
    "事前に指定されたグループを選択してください",
    ["A", "B", "C"]
    )


    if st.button("次へ"):
        if student_id == "":
            st.warning("学生番号を入力してください。")
        else:
            st.session_state.student_id = student_id
            st.session_state.field = field
            st.session_state.assigned_group = assigned_group

            # グループ別に表示される画像群を指定
            trials = trials_all[trials_all["group"] == assigned_group].sort_values("trial_order")
            st.session_state.trials = trials.to_dict("records")

            st.session_state.page = "image"
            st.session_state.image_start_time = datetime.now()
            st.rerun()

# -------------------------
# 画像回答画面
# -------------------------
elif st.session_state.page == "image":
    index = st.session_state.image_index

    trial = st.session_state.trials[index]
    st.write(f"画像 {index + 1} / {len(st.session_state.trials)}")
    st.image(trial["image_file"])

    answer = st.text_area("画像を見て座標を回答してください。", key=f"answer_{index}")

    if st.button("次の画像へ", disabled=st.session_state.submitted):

        # 回答空欄チェック
        if answer.strip() == "":
            st.warning("回答を入力してください。")
            st.stop()

        # 二重送信防止
        st.session_state.submitted = True
            
        button_time = datetime.now()

        true_answer = trial["true_answer"]
        
        try:
            response_num = float(answer)
            true_num = float(true_answer)
            
            abs_error = abs(response_num - true_num)
            correct = int(response_num == true_num)
            
        except:
            abs_error = ""
            correct = ""

        st.session_state.answers.append({
            "participant_id": st.session_state.student_id,
            "assigned_group": st.session_state.assigned_group,
            "trial_order": trial["trial_order"],
            "series_id": trial["series_id"],
            "condition": trial["condition"],
            "task": trial["task"],
            "image_file": trial["image_file"],
            "true_answer": trial["true_answer"],
            "response": answer,
            "correct": correct,
            "abs_error": abs_error,
            "image_start_time": st.session_state.image_start_time,
            "button_time": button_time,
            "display_seconds": (
                button_time - st.session_state.image_start_time
            ).total_seconds()
        })
        
        if index < len(st.session_state.trials) - 1:
            st.session_state.image_index += 1
            st.session_state.image_start_time = datetime.now()
            st.session_state.submitted = False
            st.rerun()
        else:
            save_to_google_sheets()
            st.session_state.page = "end"
            st.session_state.submitted = False
            st.rerun()

# -------------------------
# 終了画面
# -------------------------
elif st.session_state.page == "end":
    st.success("終了です。ご協力いただきありがとうございました。")
    st.write("回答はGoogleスプレッドシートに保存されました。")

    st.write("学生番号：", st.session_state.student_id)
    st.write("文理選択：", st.session_state.field)
    
    st.write("### 回答一覧")

    for item in st.session_state.answers:
        st.write(f"試行 {item['trial_order']}")
        st.write("系列ID：", item["series_id"])
        st.write("条件：", item["condition"])
        st.write("回答：", item["response"])
        st.write("表示時間（秒）：", item["display_seconds"])
        st.write("---")


