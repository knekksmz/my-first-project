import streamlit as st
import json
import os

# 画面全体の設定（ブラウザのタブ名やアイコンも設定できます！）
st.set_page_config(
    page_title="My ToDo & Memo",
    page_icon="☕",
    layout="wide"
)

# 【追加】デザインを整えるための魔法のコード（CSS）
st.markdown("""
<style>
    /* 全体の背景色をほんのり優しいオフホワイトに */
    .stApp {
        background-color: #FAFAFB;
    }
    /* ボタンを少し丸くして、今っぽいアプリ風に */
    div.stButton > button:first-child {
        border-radius: 20px;
        font-weight: bold;
        transition: all 0.3s;
    }
    /* ボタンにカーソルを合わせたときに少し浮き上がるエフェクト */
    div.stButton > button:first-child:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
</style>
""", unsafe_allow_html=True)

# タイトル周りをおしゃれに
st.title("☕ My ToDo & スケジュール")
st.markdown("日々のタスクや旅行の計画を、すっきり管理しましょう。")
st.write("") # 少し隙間を空ける

DATA_FILE = "todos.json"

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
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
            "title": "週末ランチのお店を探す",
            "detail": "奥さんと一緒に行ける、落ち着いた雰囲気のカフェか和食のお店をリサーチする。"
        }
    ]

def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

if "todos" not in st.session_state:
    st.session_state.todos = load_data()

if "selected_index" not in st.session_state:
    st.session_state.selected_index = None

col1, col2 = st.columns([1, 1])

# ＝＝＝ 左半分の画面（リスト一覧） ＝＝＝
with col1:
    st.subheader("📋 タスク一覧")
    
    # 入力欄を「カード（枠線）」で囲んでスッキリさせる
    with st.container(border=True):
        new_todo = st.text_input("新しいタスクを入力:")
        if st.button("＋ 追加する"):
            if new_todo:
                st.session_state.todos.append({"title": new_todo, "detail": ""})
                save_data(st.session_state.todos)
                st.rerun()
            
    st.write("") # 隙間を空ける

    for i, todo in enumerate(st.session_state.todos):
        # 各リストも「カード（枠線）」で囲んで見やすく！
        with st.container(border=True):
            c_title, c_detail, c_done = st.columns([3, 1, 1])
            with c_title:
                # 文字を少し強調
                st.markdown(f"**{todo['title']}**")
            with c_detail:
                if st.button("詳細 📝", key=f"detail_{i}"):
                    st.session_state.selected_index = i
                    st.rerun()
            with c_done:
                if st.button("完了 ✅", key=f"done_{i}"):
                    st.session_state.todos.pop(i)
                    if st.session_state.selected_index == i:
                        st.session_state.selected_index = None
                    save_data(st.session_state.todos)
                    st.rerun()

# ＝＝＝ 右半分の画面（詳細メモ） ＝＝＝
with col2:
    st.subheader("📝 詳細・メモ")
    
    if st.session_state.selected_index is not None:
        idx = st.session_state.selected_index
        if idx < len(st.session_state.todos):
            target_todo = st.session_state.todos[idx]
            
            # メモ欄もカードで囲む
            with st.container(border=True):
                st.markdown(f"### {target_todo['title']}")
                
                updated_detail = st.text_area("詳細スケジュールやメモを編集:", value=target_todo['detail'], height=300)
                
                if st.button("💾 メモを保存"):
                    st.session_state.todos[idx]['detail'] = updated_detail
                    save_data(st.session_state.todos)
                    st.success("保存しました！")
    else:
        st.info("👈 左のリストから「詳細 📝」ボタンを押すと、ここにメモが表示されます。")
