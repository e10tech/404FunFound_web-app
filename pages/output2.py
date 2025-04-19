import streamlit as st
from elevenlabs import ElevenLabs, play #ElevenLabs APIの利用に必要
from io import BytesIO  #ElevenLabsで作成した合成音声をバイト型に変換
from dotenv import load_dotenv  #.envファイルの読み込みに必要なモジュール
from streamlit_extras.switch_page_button import switch_page
import base64
import requests
import os   #.envから環境設定変数を取得するために必要

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

st.container(height=5, border=False)

col1, col2, col3 = st.columns([1, 2, 1])
with col1:
    if st.button("📖 前のページへ", use_container_width=True):
        switch_page("output1")  # pages/output1.py に遷移する
with col3:
    if st.button("📖 次のページへ", use_container_width=True):
        switch_page("output3")  # pages/output3.py に遷移する
    
with st.container():
    #画像を挿入したい時に使う
    #変数から画像を取得する
    st.image("./picture/story2.jpg")

    ##合成音声の組み込み（にじボイスAPI）
    #url = "https://api.nijivoice.com/api/platform/v1/voice-actors/294eeefe-f46c-45a6-9e5a-e6a3b3d6eb6e/generate-voice"

    #payload = {
    #    "format": "mp3",
    #    "script": "ある日夜空に光る星たちと、おりがみの花に囲まれて、ルナはそっと願いごとをささやいた。「いつか、星の国に行けますように…」",
    #    "speed": "1",
    #    "emotionalLevel": "0.1",
    #    "soundDuration": "0.1"
    #}
    #headers = {
    #    "accept": "application/json",
    #    "x-api-key": os.getenv("x-api-key"),
    #    "content-type": "application/json"
    #}
    #response = requests.post(url, json=payload, headers=headers)

    #result = response.json()
    #audio_data = result['generatedVoice']['audioFileUrl']
    #st.audio(audio_data, format="audio/mp3", loop=False)

    #音声合成を変数からもってくる
    st.audio(
        'https://storage.googleapis.com/ai-voice-prod-storage/platform/c37e784d-25b1-403b-a4a1-34dc6debc145/voices/2025/04/13/be119c37-225c-4e2c-8a0e-6301a751a45e/uploaded-audio.mp3?GoogleAccessId=ai-voice-api-prod-sa%40algomatic-global-ai-voice.iam.gserviceaccount.com&Expires=1744608807&Signature=mhiyIsFU5%2F0f0uoIRVIWynPVhn1mcaeYWO5m6QlELfhN6WhgsuPXjZy9bv5T%2By0Nhu9dzeIFehxX5UEdCKzxlbc3LqA5lNfs2Kx5u5pQgx3M8%2FHb%2BKRK4Luz4GI8t2ck%2By5q%2FE9GTpQxnXcd5XA0fIc2eFsPfZdhmwEowg5lpL%2Br16u%2BWokYk38ibqcDaHn9M3%2B4ANfWhnUaeWIvJGfH4F8swaf1vWKhecTrvRybk%2FustxRU8gv14vNHWIE93JUj7T6KNscTXtEK3WAgqaAPo5oUbe7qgcQe4ysd5ALAKxowpijKUJj%2BNb2InfMAZo04cvOhCKCwzG1CzZhlmuydaw%3D%3D',
        format="audio/mp3",
        loop=False
    )
    #エキスパンダーでテキストを表示
    #テキストも変数から引っ張ってくる
    expander = st.expander("テキストを表示")
    expander.write("わるいりゅうが　おしろをおそってきたよ！")

#ダウンロード機能の組み込み
st.download_button(
    label="Download Image",
    data="",
    file_name='book.jpg',
    icon=":material/download:"
)

#特定の変数に今のページがどこかを記載しておく
#page = 2[3枚目用]が欲しい→ハードコーディング
#3枚目の画像を生成するコードがここに入る
#これがGitHubのoutputフォルダに入るイメージ

#3枚目のにじボイスのAPIで音声を作成するコードの実行
#これがGitHubのoutputフォルダに入るイメージ

#次へボタンが表示されて3枚目にいけるようにする