import streamlit as st

# 画面を横広く使う設定
st.set_page_config(layout="wide")

st.title("✅ やりたいことリスト（詳細メモ付き）")

# データを「タイトル」と「詳細」のセットに変更
if "todos" not in st.session_state:
    st.session_state.todos = [
        {
            "title": "5月の北海道旅行の計画を立てる",
            "detail": "【日程】2026年5月2日〜5月5日\n【予算】1人あたり15万円\n\n■ 5月2日\n10:00 新千歳空港着\n12:00 札幌でランチ\n\n■ 5月3日\n08:00 朝食バイキング\n..."
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

# どのタスクの詳細を見ているか（選択中の番号）を記憶する準備
if "selected_index" not in st.session_state:
    st.session_state.selected_index = None

# 画面を左右に分割 (左:col1, 右:col2)
col1, col2 = st.columns([1, 1])

# ＝＝＝ 左半分の画面（リスト一覧） ＝＝＝
with col1:
    st.subheader("📋 タスク一覧")
    
    # 新しいタスクの追加
    new_todo = st.text_input("新しいやりたいことを入力:")
    if st.button("追加"):
        if new_todo:
            st.session_state.todos.append({"title": new_todo, "detail": ""})
            st.rerun()
            
    st.divider()

    # リストの表示
    for i, todo in enumerate(st.session_state.todos):
        # ボタンを横に並べるためにさらに分割
        c_title, c_detail, c_done = st.columns([3, 1, 1])
        with c_title:
            st.write(f"・ {todo['title']}")
        with c_detail:
            # 詳細ボタンを押したら、その番号を記憶して画面を更新
            if st.button("詳細", key=f"detail_{i}"):
                st.session_state.selected_index = i
                st.rerun()
        with c_done:
            # 完了ボタンを押したらリストから削除
            if st.button("完了", key=f"done_{i}"):
                st.session_state.todos.pop(i)
                if st.session_state.selected_index == i:
                    st.session_state.selected_index = None
                st.rerun()

# ＝＝＝ 右半分の画面（詳細メモ） ＝＝＝
with col2:
    st.subheader("📝 詳細・スケジュール")
    
    # もし何かの「詳細」ボタンが押されていたら
    if st.session_state.selected_index is not None:
        idx = st.session_state.selected_index
        # エラー防止のチェック
        if idx < len(st.session_state.todos):
            target_todo = st.session_state.todos[idx]
            
            st.markdown(f"**【 {target_todo['title']} 】**")
            
            # 自由に書き込めるテキストエリア
            updated_detail = st.text_area("メモを編集:", value=target_todo['detail'], height=300)
            
            if st.button("メモを保存"):
                st.session_state.todos[idx]['detail'] = updated_detail
                st.success("保存しました！")
    else:
        st.info("👈 左のリストから「詳細」ボタンを押すと、ここにスケジュールの内訳やメモを書き込めます。")
