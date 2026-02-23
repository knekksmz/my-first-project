import streamlit as st

# アプリのタイトル
st.title("✅ やりたいことリスト")

# データを保存するための準備
if "todos" not in st.session_state:
    st.session_state.todos = [
        "5月の北海道旅行の計画を立てる",
        "人事（HR）関連の書籍を読む",
        "自由が丘で週末ランチのお店を探す"
    ]

# 新しいタスクを入力する欄
new_todo = st.text_input("新しいやりたいことを入力してください:")

# 追加ボタン
if st.button("追加"):
    if new_todo:
        st.session_state.todos.append(new_todo)
        st.rerun()

st.divider()

# リストの表示と完了ボタン
for i, todo in enumerate(st.session_state.todos):
    col1, col2 = st.columns([4, 1])
    with col1:
        st.write(f"・ {todo}")
    with col2:
        if st.button("完了", key=f"done_{i}"):
            st.session_state.todos.pop(i)
            st.rerun()
