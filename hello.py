import streamlit as st
import json
import os

# 画面を横広く使う設定
st.set_page_config(layout="wide")
st.title("✅ やりたいことリスト（詳細メモ付き）")

# データ保存用のファイル名を設定
DATA_FILE = "todos.json"

# 【追加】ファイルからデータを読み込む関数
def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    # ファイルがまだない場合（最初）のデータ
    return [
        {
            "title": "5月の北海道旅行の計画を立てる",
            "detail": "【日程】2026年5月2日〜5月5日\n【予算】1人あたり15万円\n\n■ 5月2日\n10:00 新千歳空港着\n12:00 札幌でランチ\n\n■ 5月3日\n08:00 朝食バイキング"
        },
        {
            "title": "ビジネス書・自己啓発本を読む",
            "detail": "『7つの習慣』や『嫌われる勇気』の要約を読み直して、今後のキャリアの参考にする。"
        },
        {
            "title": "自由が丘で週末ランチのお店を探す",
            "detail": "奥さんと一緒に行ける、落ち着いた雰囲気のカフェか和食のお店をリサーチする。"
        }
    ]

# 【追加】ファイルにデータを書き込んで保存する関数
def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

# アプリを開いた時に、保存されているデータを読み込む
if "todos" not in st.session_state:
    st.session_state.todos = load_data()

if "selected_index" not in st.session_state:
    st.session_state.selected_index = None

col1, col2 = st.columns([1, 1])

# ＝＝＝ 左半分の画面（リスト一覧） ＝＝＝
with col1:
    st.subheader("📋 タスク一覧")
    
    new_todo = st.text_input("新しいやりたいことを入力:")
    if st.button("追加"):
        if new_todo:
            st.session_state.todos.append({"title": new_todo, "detail": ""})
            save_data(st.session_state.todos) # 👈 追加した時にファイルに保存
            st.rerun()
            
    st.divider()

    for i, todo in enumerate(st.session_state.todos):
        c_title, c_detail, c_done = st.columns([3, 1, 1])
        with c_title:
            st.write(f"・ {todo['title']}")
        with c_detail:
            if st.button("詳細", key=f"detail_{i}"):
                st.session_state.selected_index = i
                st.rerun()
        with c_done:
            if st.button("完了", key=f"done_{i}"):
                st.session_state.todos.pop(i)
                if st.session_state.selected_index == i:
                    st.session_state.selected_index = None
                save_data(st.session_state.todos) # 👈 完了（削除）した時にファイルに保存
                st.rerun()

# ＝＝＝ 右半分の画面（詳細メモ） ＝＝＝
with col2:
    st.subheader("📝 詳細・スケジュール")
    
    if st.session_state.selected_index is not None:
        idx = st.session_state.selected_index
        if idx < len(st.session_state.todos):
            target_todo = st.session_state.todos[idx]
            
            st.markdown(f"**【 {target_todo['title']} 】**")
            
            updated_detail = st.text_area("メモを編集:", value=target_todo['detail'], height=300)
            
            if st.button("メモを保存"):
                st.session_state.todos[idx]['detail'] = updated_detail
                save_data(st.session_state.todos) # 👈 メモを編集した時にファイルに保存
                st.success("保存しました！")
    else:
        st.info("👈 左のリストから「詳細」ボタンを押すと、ここにスケジュールの内訳やメモを書き込めます。")
