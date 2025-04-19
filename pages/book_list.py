import streamlit as st
import pandas as pd

#ページ設定を行う。サイトのタイトルやアイコン、画面幅を設定する
#おそらくファイルの一番初めに記載しておかないといけないみたい
st.set_page_config(
        page_title="おはなしたからばこ",
        page_icon="📕",
        layout="wide",
    )

#画面全体に色や背景画像を設定する
st.markdown(
    """
    <style>
    .stApp {
        background-color: #dcfaf9;
    }
    .block-container {
        padding-top: 1rem;
    }
    header, footer {
        visibility: hidden;
    }
    </style>
    """,
    unsafe_allow_html=True
)

#サイドバーを表示させる
with st.sidebar:
    st.image("./picture/side_logo.png")
    st.markdown("""
                <a href="/input" target="_self">
                    <button style='font-size:18px; padding:0.5em 1em; border-radius:8px; background-color:#4CAF50; color:white; border:none;'>
                        📖 すきな絵本（えほん）をつくる
                    </button>
                </a>
            """, unsafe_allow_html=True)
    st.container(height=10, border=False)
    st.markdown("""
                <a href="/book_list" target="_self">
                    <button style='font-size:18px; padding:0.5em 1em; border-radius:8px; background-color:#4CAF50; color:white; border:none;'>
                        📖 むかしの本（ほん）からつくる
                    </button>
                </a>
            """, unsafe_allow_html=True)
    st.container(height=10, border=False)
    st.markdown("""
                <a href="" target="_self">
                    <button style='font-size:18px; padding:0.5em 1em; border-radius:8px; background-color:#4CAF50; color:white; border:none;'>
                        使い方を見る
                    </button>
                </a>
            """, unsafe_allow_html=True)

with st.container(border=False):
    st.image('./picture/title_logo.png')
    st.container(height=10, border=False)

##スクレイピングした書籍情報をまとめたcsvからタイトル等の情報を取得
df = pd.read_csv('./book_total.csv')
#重複行を削除
drop_df = df.drop_duplicates(subset=['書籍タイトル'])

#書籍の書く情報をリスト化
title_list = drop_df['書籍タイトル'].tolist()
image_list = drop_df['画像URL'].tolist()
brief_list = drop_df['要約_和'].tolist()

col1, col2, col3 = st.columns([1, 2, 1])
with col3:
    st.markdown("""
                <a href="main" target="_self">
                    <button style='font-size:18px; padding:0.5em 1em; border-radius:8px; background-color:#4CAF50; color:white; border:none; width:100%;'>
                        🏠 ホーム
                    </button>
                </a>
            """, unsafe_allow_html=True)
st.container(height=10, border=False)

row1 = st.columns(2, gap="large")
st.container(height=10, border=False)
row2 = st.columns(2, gap="large")
col = row1 + row2

for i, name in enumerate(title_list):
    with col[i]:
        if st.button(name, use_container_width=True):
            st.session_state.book_selected = name
        st.image(image_list[i], use_container_width=True)
        st.write(brief_list[i])
        
st.container(height=10, border=False)
st.markdown("""
                <a href="/output1" target="_self">
                    <button style='font-size:18px; padding:0.5em 1em; border-radius:8px; background-color:#4CAF50; color:white; border:none; width:100%;'>
                        📖 作成する
                    </button>
                </a>
            """, unsafe_allow_html=True)
