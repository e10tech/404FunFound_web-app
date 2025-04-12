import streamlit as st  #streamlitの使用に必要
from elevenlabs import ElevenLabs, play #ElevenLabs APIの利用に必要
from io import BytesIO  #ElevenLabsで作成した合成音声をバイト型に変換
from dotenv import load_dotenv  #.envファイルの読み込みに必要なモジュール
import base64
import os   #.envから環境設定変数を取得するために必要

from page_info import input_page, output_page   #page_info.pyに記載した関数をインポート

#初期化(session_stateのセット)
if "page" not in st.session_state:
    st.session_state.page = 'input_page'
if "user_name" not in st.session_state:
    st.session_state.user_name = ''

#ページ表示の制御
if st.session_state.page == "input_page":
    input_page()
elif st.session_state.page == "output_page":
    output_page()