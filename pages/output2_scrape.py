import streamlit as st
import pandas as pd
import os
import sys
import json
from dotenv import load_dotenv
import requests
from scrap_story import voice_generated as vg
from scrap_story import generate_image
from openai import OpenAI

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

col1, col2, col3 = st.columns([1, 2, 1])
with col3:
    st.markdown("""
                <a href="main" target="_self">
                    <button style='font-size:18px; padding:0.5em 1em; border-radius:8px; background-color:#4CAF50; color:white; border:none; width:100%;'>
                        🏠 ホーム
                    </button>
                </a>
            """, unsafe_allow_html=True)
    
with st.container():
    #画像を挿入したい時に使う
    #変数から画像を取得する
    st.image("./output/1.jpeg")

    #音声合成を変数からもってくる
    st.audio(
        "./output/voice1.mp3",
        format="audio/mp3",
        loop=False
    )
    #エキスパンダーでテキストを表示
    #テキストも変数から引っ張ってくる
    expander = st.expander("テキストを表示")
    expander.write(st.session_state.audio_text[1])

#ダウンロード機能の組み込み
st.download_button(
    label="Download Image",
    data="",
    file_name='book.jpg',
    icon=":material/download:"
)


#3枚目の画像と音声をを生成するコードがここに入る
#まずは今のページを宣言
now_page = 2

#画像を生成
#st.write('画像生成を行います')
generate_image(st.session_state.story, now_page)
#st.write('画像生成が完了しました')

#音声を生成
#st.write('音声生成を行います')
id ='d158278c-c4fa-461a-b271-468146ad51c9'
vg(id, st.session_state.audio_text[now_page], now_page)
#st.write('音声生成が完了しました')

#次へボタンが表示されて2枚目にいけるようにする
st.container(height=5, border=False)

col1, col2, col3 = st.columns([1, 2, 1])
with col3:
    if st.button("📖 次のページへ", use_container_width=True):
        st.switch_page("pages/output3_scrape.py")  # pages/output3_scrape.py に遷移する