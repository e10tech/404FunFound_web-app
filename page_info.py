import streamlit as st
from elevenlabs import ElevenLabs, play #ElevenLabs APIの利用に必要
from io import BytesIO  #ElevenLabsで作成した合成音声をバイト型に変換
from dotenv import load_dotenv  #.envファイルの読み込みに必要なモジュール
import base64
import requests
import os   #.envから環境設定変数を取得するために必要

#ページ遷移用の関数
def go_to_page(page_name):
    st.session_state.page = page_name

#インプットページのコーディング
def input_page():
    st.set_page_config(
        page_title="アプリ名",
        page_icon="📕",
        layout="wide"
    )
    #画面全体に色や背景画像を設定する
    st.markdown(
        """
        <style>
        .stApp {
            background-color: #fcefe1;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    #サイドバーを表示させる
    st.sidebar.title("アプリ名orアプリロゴ")
    st.sidebar.button("絵本を作る", on_click=go_to_page, args=('input_page',), use_container_width=True)
    st.sidebar.button("使い方を見る", use_container_width=True)

    st.markdown(
        """
        <style>
        .centered-title {
            text-align: center;
            font-size: 48px;
            font-weight: bold;
            margin: 20px 0px;
        }
        </style>
        <div class='centered-title'>Webアプリ名</div>
        """,
        unsafe_allow_html=True
    )

    

    #画像生成におけるpreset_typeを選択
    preset_options = [
        {"id" : "anime", "label" : "アニメ風"},
        {"id" : "enhance", "label" : "enhanceって何？"},
        {"id" : "isometric", "label" : "立体感"},
        {"id" : "photographic", "label" : "写真風"},
    ]
    #containerの枠線を消す
    st.markdown("""
    <style>
        div[data-testid="stVerticalBlock"] > div {
            border: none !important;
            box-shadow: none !important;
        }
    </style>
    """, unsafe_allow_html=True)

    with st.container(height=250):
        st.markdown("<h4 style='color:#634320;'>どんな感じのイラストを作る？</h4>", unsafe_allow_html=True)
        # カード表示
        cols = st.columns(len(preset_options))

        selected_id = None
        for i, option in enumerate(preset_options):
            with cols[i]:
                st.image("./picture.png")
                if st.button(option["label"], use_container_width=True):
                    st.session_state.preset_selected = option["id"]
        #preset_selected = st.selectbox(
        #    "選択肢",
        #    preset_options,
        #    format_func=lambda x: x["label"]
        #)

    #画像生成における物語のテーマを選択
    theme_options = [
        {"id" : "1", "label" : "ワクワクする物語"},
        {"id" : "2", "label" : "ドキドキする物語"},
        {"id" : "3", "label" : "ファンタジー"},
        {"id" : "4", "label" : "SF（サイエンス・フィクション）"},
    ]
    with st.container(height=250):
        st.markdown("<h4 style='color:#634320;'>どんな絵本を作る？</h4>", unsafe_allow_html=True)
        theme_selected = st.selectbox(
            "選択肢",
            theme_options,
            format_func=lambda x: x["label"]
        )

    st.button('作成する', on_click=go_to_page, args=('output_page',), use_container_width=True)


#アウトプットページのコーディング
def output_page():
    #ページ設定を行う。サイトのタイトルやアイコン、画面幅を設定する
    #おそらくファイルの一番初めに記載しておかないといけないみたい
    st.set_page_config(
        page_title="アプリ名",
        page_icon="📕",
        layout="wide"
    )
    #画面全体に色や背景画像を設定する
    st.markdown(
        """
        <style>
        .stApp {
            background-color: #fcefe1;
        }
        </style>
        """,
        unsafe_allow_html=True
    )
    #サイドバーを表示させる
    st.sidebar.title("アプリ名orアプリロゴ")
    st.sidebar.button("絵本を作る", on_click=go_to_page, args=('input_page',), use_container_width=True)
    st.sidebar.button("使い方を見る", use_container_width=True)

    #.envファイルの読み込み
    load_dotenv()

    col1, col2, col3 = st.columns([1, 2, 1])
    with col3:
        st.button('ホームに戻る', on_click=go_to_page, args=('input_page',), use_container_width=True)

    col1, col2, col3 = st.columns([1, 2, 1])
    with col1:
        st.button('前のページに戻る', use_container_width=True)
    with col3:
        st.button('次のページに進む', use_container_width=True)
    
    #画像を挿入したい時に使う
    st.image("v1_txt2img_0.png")

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

    #エキスパンダーでテキストを表示
    expander = st.expander("テキストを表示")
    expander.write("ある日夜空に光る星たちと、おりがみの花に囲まれて、ルナはそっと願いごとをささやいた。「いつか、星の国に行けますように…」")

    #フィードバック機能の組み込み
    sentiment_mapping = ["one", "two", "three", "four", "five"]
    selected = st.feedback("stars")

    #ダウンロード機能の組み込み
    st.download_button(
        label="Download Book",
        data="",
        file_name='book.jpg',
        icon=":material/download:"
    )