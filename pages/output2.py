import streamlit as st
# from elevenlabs import ElevenLabs, play #ElevenLabs APIの利用に必要
# from io import BytesIO  #ElevenLabsで作成した合成音声をバイト型に変換
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

#3枚目の画像を生成するコードがここに入る
#これがGitHubのoutputフォルダに入るイメージ←githubへの入れ方分からなかった。streamlitクラウドに期待
page = 2 # ハードコーディングでok
yochan.make_image_stability(st.session_state.story, st.session_state.preset, page)

#3枚目のにじボイスのAPIで音声を作成するコードの実行
#これがGitHubのoutputフォルダに入るイメージ
vg(st.session_state.voice, st.session_state.audio_text, page)

#次へボタンが表示されて3枚目にいけるようにする
st.container(height=5, border=False)

col1, col2, col3 = st.columns([1, 2, 1])
#with col1:
#    if st.button("📖 前のページへ", use_container_width=True):
#        st.switch_page("pages/output1.py")  # pages/output1.py に遷移する
with col3:
    if st.button("📖 次のページへ", use_container_width=True):
        st.switch_page("pages/output3.py")  # pages/output3.py に遷移する