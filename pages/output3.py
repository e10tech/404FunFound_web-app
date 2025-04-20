import streamlit as st
from elevenlabs import ElevenLabs, play #ElevenLabs APIの利用に必要
from io import BytesIO  #ElevenLabsで作成した合成音声をバイト型に変換
from dotenv import load_dotenv  #.envファイルの読み込みに必要なモジュール
from streamlit_extras.switch_page_button import switch_page
import base64
import requests
import os   #.envから環境設定変数を取得するために必要
import yochanchanco as yochan
from voice import voice_generated as vg

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
    #画像を変数から取得し下記URLに変換する
    st.image("./output/2.jpeg")

    #音声を変数から取得し下記URLに変換する
    st.audio(
        'https://storage.googleapis.com/ai-voice-prod-storage/platform/c37e784d-25b1-403b-a4a1-34dc6debc145/voices/2025/04/13/be119c37-225c-4e2c-8a0e-6301a751a45e/uploaded-audio.mp3?GoogleAccessId=ai-voice-api-prod-sa%40algomatic-global-ai-voice.iam.gserviceaccount.com&Expires=1744608807&Signature=mhiyIsFU5%2F0f0uoIRVIWynPVhn1mcaeYWO5m6QlELfhN6WhgsuPXjZy9bv5T%2By0Nhu9dzeIFehxX5UEdCKzxlbc3LqA5lNfs2Kx5u5pQgx3M8%2FHb%2BKRK4Luz4GI8t2ck%2By5q%2FE9GTpQxnXcd5XA0fIc2eFsPfZdhmwEowg5lpL%2Br16u%2BWokYk38ibqcDaHn9M3%2B4ANfWhnUaeWIvJGfH4F8swaf1vWKhecTrvRybk%2FustxRU8gv14vNHWIE93JUj7T6KNscTXtEK3WAgqaAPo5oUbe7qgcQe4ysd5ALAKxowpijKUJj%2BNb2InfMAZo04cvOhCKCwzG1CzZhlmuydaw%3D%3D',
        format="audio/mp3",
        loop=False
    )
    #エキスパンダーでテキストを表示
    #テキストも変数から引っ張ってくる
    expander = st.expander("テキストを表示")
    expander.write("こわくても　ゆうきをだして　たたかうよ！")

#ダウンロード機能の組み込み
st.download_button(
    label="Download Image",
    data="",
    file_name='book.jpg',
    icon=":material/download:"
)

#4枚目の画像を生成するコードがここに入る
#これがGitHubのoutputフォルダに入るイメージ←githubへの入れ方分からなかった。streamlitクラウドに期待
page = 3 # ハードコーディングでok
yochan.make_image_stability(st.session_state.story, st.session_state.preset, page)

#4枚目のにじボイスのAPIで音声を作成するコードの実行
#これがGitHubのoutputフォルダに入るイメージ
vg(st.session_state.voice, st.session_state.audio_text, page)

#次へボタンが表示されて4枚目にいけるようにする
st.container(height=5, border=False)

col1, col2, col3 = st.columns([1, 2, 1])
#with col1:
#    if st.button("📖 前のページへ", use_container_width=True):
#        st.switch_page("pages/output2.py")  # pages/output2.py に遷移する
with col3:
    if st.button("📖 次のページへ", use_container_width=True):
        st.switch_page("pages/output4.py")  # pages/output4.py に遷移する