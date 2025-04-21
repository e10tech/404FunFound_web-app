import streamlit as st
import pandas as pd
import os
import sys
import json
from dotenv import load_dotenv
import requests
from scrap_story import make_story
from scrap_story import voice_generated as vg
from scrap_story import generate_image
from scrap_story import make_image_prompt_gpt
from openai import OpenAI

#環境変数の読み込み
load_dotenv()

#ページ設定を行う。サイトのタイトルやアイコン、画面幅を設定する
#ここがあるとエラーになるので一旦コメントアウトします
#おそらくファイルの一番初めに記載しておかないといけないみたい
# st.set_page_config(
#         page_title="おはなしたからばこ",
#         page_icon="📕",
#         layout="wide",
#     )

"""
ここ追加してます
このページ中に起承転結ストーリー
1枚目画像、1枚目音声をつくるために必要
"""

#APIキーの取得→openaiのAPIキー
openai_api_key = os.getenv('OPENAI_API_KEY')
if openai_api_key is None:
    print("Error: OPENAI_API_KEY is not set in the environment variables.")
    sys.exit(1)

#APIキーの取得→stable diffusionのAPIキー
stability_api_key = os.getenv('STABILITY_API_KEY')
if stability_api_key is None:
    print("Error: STABILITY_API_KEY is not set in the environment variables.")
    sys.exit(1)

#APIキーの取得→にじボイスのAPIキー
x_api_key = os.getenv('x_api_key')
if x_api_key is None:
    print("Error: X_API_KEY is not set in the environment variables.")
    sys.exit(1)

"""
ここ追加してます
まずは空のセッションステートを定義
"""
# アプリの早い段階でセッション変数を初期化
if "book_selected" not in st.session_state:
    st.session_state.book_selected = None  # または適切なデフォルト値
if 'audio_text' not in st.session_state:
    st.session_state.audio_text = None
if 'story' not in st.session_state:
    st.session_state.story = None

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
drop_df = df.drop_duplicates(subset=['書籍タイトル_日'])

#書籍の書く情報をリスト化
title_list = drop_df['書籍タイトル_日'].tolist()
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

"""
選択した物語を記憶しておく
"""
df_select = df[df['書籍タイトル_日'] == st.session_state.book_selected]

# st.container(height=10, border=False)
# st.markdown("""
#                 <a href="/output1_scrape" target="_self">
#                     <button style='font-size:18px; padding:0.5em 1em; border-radius:8px; background-color:#4CAF50; color:white; border:none; width:100%;'>
#                         📖 絵本をみにいく
#                     </button>
#                 </a>
#             """, unsafe_allow_html=True)


now_page = 0

if "is_ready" not in st.session_state:
    st.session_state.is_ready = False

if st.button("📖 絵本（えほん）をつくる", use_container_width=True):
    #st.write('テスト用：データフレームを表示します')
    #st.dataframe(df_select)

    #起承転結ストーリーを作成する前準備と実行
    #story = []#空のリストを定義する
    #st.write('テスト用：空のリスト型を作成しました')
    chapter_text = df_select['本文'][0]#引数に必要なので
    #st.write('テスト用：本文を取得しました起承転結を作成します')
    story = make_story(chapter_text, openai_api_key)
    #storyはリスト型のひらがなのおはなし
    st.session_state.audio_text = story

    #ストーリー用の画像生成プロンプトを生成する関数の実行
    image_prompts =[]
    #st.write('テスト用：画像生成用の空リストを作成')
    image_prompts = make_image_prompt_gpt(story, openai_api_key)
    st.session_state.story = image_prompts
    #st.write('画像生成のプロンプトリストを生成できました')

    #現在のページを定義する
    page = 0
    #起の画像生成をする関数の実行
    generate_image(image_prompts, page)
    #st.write('1枚目の画像を生成できました')

    #合成音声を生成する関数の実行
    #こちらの既存の物語からの機能は音声id固定
    #st.write('音声合成を行います')
    id ='d158278c-c4fa-461a-b271-468146ad51c9'
    vg(id, story[page], 0)
    #st.write('すべてのapiが実行されました')

    # すべてのAPIが完了したらフラグを立てる
    st.session_state.is_ready = True

#↓これはページの切り替えの動作のトリガーにする
if st.session_state.is_ready:
    if st.button("📖 準備ができたので読みに行く", use_container_width=True):
        st.switch_page("pages/output1_scrape.py")  # pages/output1.py に遷移する