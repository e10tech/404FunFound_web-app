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
    #画面全体に色や背景画像を設定する  background-color: #fcefe1;
    st.markdown(
        """
        <style>
        .stApp {
            background-image: url("https://i.ibb.co/dwLByZ52/picture.png");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
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

    #containerの枠線を消す
    st.markdown("""
    <style>
        div[data-testid="stVerticalBlock"] > div {
            border: none !important;
            box-shadow: none !important;
        }
    </style>
    """, unsafe_allow_html=True)

    #画像生成におけるpreset_typeを選択
    preset_options = [
        {"id" : "anime", "label" : "アニメ風"},
        {"id" : "enhance", "label" : "enhanceって何？"},
        {"id" : "isometric", "label" : "立体感"},
        {"id" : "photographic", "label" : "写真風"},
    ]    
    with st.container(height=230):
        st.markdown("<h4 style='color:#634320;'>どんな感じのイラストを作る？</h4>", unsafe_allow_html=True)
        # カード表示
        cols = st.columns(len(preset_options))

        preset_selected = None
        for i, preset_option in enumerate(preset_options):
            with cols[i]:
                st.image("./picture.png")
                if st.button(preset_option["label"], use_container_width=True):
                    st.session_state.preset_selected = preset_option["id"]
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
        {"id" : "4", "label" : "SF"},
    ]
    with st.container(height=130):
        st.markdown("<h4 style='color:#634320;'>どんな絵本を作る？</h4>", unsafe_allow_html=True)
        # カード表示
        cols = st.columns(len(theme_options))

        theme_selected = None
        for i, theme_option in enumerate(theme_options):
            with cols[i]:
                if st.button(theme_option["label"], use_container_width=True):
                    st.session_state.theme_selected = theme_option["id"]

    #with st.container(height=250):
    #    st.markdown("<h4 style='color:#634320;'>どんな絵本を作る？</h4>", unsafe_allow_html=True)
    #    theme_selected = st.selectbox(
    #        "選択肢",
    #        theme_options,
    #        format_func=lambda x: x["label"]
    #    )

    #読み上げボイスを選択
    voice_options = [
        {"id" : "294eeefe-f46c-45a6-9e5a-e6a3b3d6eb6e", "data" : {"label" : "知的", "audio" : 'https://storage.googleapis.com/ai-voice-prod-storage/platform/c37e784d-25b1-403b-a4a1-34dc6debc145/voices/2025/04/13/d5dd46e1-7ce2-4245-8055-055363eff186/uploaded-audio.mp3?GoogleAccessId=ai-voice-api-prod-sa%40algomatic-global-ai-voice.iam.gserviceaccount.com&Expires=1744610051&Signature=gOGFMQ1z%2BUDyr7w5Kj6aCF38a1OTeu08gc6wmYHfxA5pIJJbcqPAwg4%2Fm1fXLRIunyHrqPUKDDH4xf3bUcpz4BMo3vt%2FHOgFu7KK0ngDlrCiwgVLaMDSjhJgv6q%2F8Go6QOrSERPue8K%2B7Nav05b9sNLgmEvtypMFvLPK7cF%2BTELxzUSF%2ByFkxLibztKG%2BdidNBpMn5O3Ni%2Bmzy7qHhoguTxLCnmrUItnA6VkQJFgPstoJn90JBb424XM5she97hXJsfSmkdCbkdzDrXPkwR5WXslJdZFl1A15jVofZPQRcUkBVK%2FSXSs7G0MJNoZRDq%2Bjc1jf%2BUi18Tuy%2BexJz2x4g%3D%3D'}},
        {"id" : "c853dd84-6fb1-41bd-b82e-303d5f35fe38", "data" : {"label" : "さわやか", "audio" : 'https://storage.googleapis.com/ai-voice-prod-storage/platform/c37e784d-25b1-403b-a4a1-34dc6debc145/voices/2025/04/13/45755f2b-ab2f-4a86-b4f4-4b23a0137126/uploaded-audio.mp3?GoogleAccessId=ai-voice-api-prod-sa%40algomatic-global-ai-voice.iam.gserviceaccount.com&Expires=1744610346&Signature=N4ORK%2BEZf6NX9yYdlFK3kJk2UZeBpLzdUPotcBYyRtHRNVA8Wf3aa5kNGitAnM%2FrIusOnVrstMZJ1%2FLlgYHpBT5ScqzmgSjk0ZykboNgLeUFhnEGkONlYE2wxLWo6iEbH11XJjaMxI%2BWkMHukwVwfbTkgYjOxnw3l895beTi0O7apjJP%2BzKAhfVQuQZ9LNqB4zUd4cnGXYxqyz4gpg0Il%2F9am%2Fk2Ayu%2B1aTGdon%2FAhp9IVs9uZvBFxqDfNWubl%2BrqSFjDGYVxEQxtY589WYCgx1ThxcbiAHDveGtyFB5gNBCog9WKS9kLZ6B%2ByAfd9iwilt2QY4FYulVwV02SA9WCw%3D%3D'}},
        {"id" : "2773f3eb-2d5e-452b-b626-59d0869c53ec", "data" : {"label" : "サンタクロース", "audio" : 'https://storage.googleapis.com/ai-voice-prod-storage/platform/c37e784d-25b1-403b-a4a1-34dc6debc145/voices/2025/04/13/4527fd13-c357-4c63-b660-018b70011ca1/uploaded-audio.mp3?GoogleAccessId=ai-voice-api-prod-sa%40algomatic-global-ai-voice.iam.gserviceaccount.com&Expires=1744610394&Signature=lKVsUrBaPrM5c6XrfK6vWp8nV8HJaZVtGa2bSNIRgyRggtqgaryLzCosL5Na51rNAKOBaHNLeqzh3b08Y9EoAUWezfLd9tHzmnb7R7IYmCsOKXJGzDRcQ%2FTx1S%2BNNg6vH8y37Nq0b4%2FVTidbbug9%2BoM%2BnYD4QghLm0MX7u8lmGXkZN7bG16eT2zGOFxOveOh36wgbmmu6PlndZvH2crMDC7hE91RsZ7NEMJZuMESyZve6m9iPHskkrV6oYPihta9zlwqPmeFHxODqTPA3OMjuXcbZo0b4FnRIYmkW57A2VA4VuocbMJN1vDJvFmatvBhF6%2BBHD8P6vgpDs1eKFUJ6A%3D%3D'}},
    ]
    with st.container(height=250):
        st.markdown("<h4 style='color:#634320;'>どんな声がいい？</h4>", unsafe_allow_html=True)
        #カード表示
        cols = st.columns(len(voice_options))

        voice_selected = None
        for i, voice_option in enumerate(voice_options):
            with cols[i]:
                if st.button(voice_option["data"]["label"], use_container_width=True):
                    st.session_state.voice_selected = voice_option["id"]
                st.write("試しに聞いてみる")
                st.audio(
                    voice_options[i]["data"]["audio"],
                    format="audio/mp3",
                    loop=False
                )


    st.button('作成する', on_click=go_to_page, args=('output_page',), icon="📖", use_container_width=True)


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
    st.sidebar.title("アプリ名orアプリロゴ")
    st.sidebar.button("絵本を作る", on_click=go_to_page, args=('input_page',), use_container_width=True)
    st.sidebar.button("使い方を見る", use_container_width=True)

    #.envファイルの読み込み
    load_dotenv()

    col1, col2, col3 = st.columns([1, 2, 1])
    with col3:
        st.button('ホームに戻る', on_click=go_to_page, args=('input_page',), icon="🏠", use_container_width=True)

    col1, col2, col3 = st.columns([1, 2, 1])
    with col1:
        st.button('前のページに戻る', use_container_width=True)
    with col3:
        st.button('次のページに進む', use_container_width=True)
    
    with st.container():
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

        st.audio(
            'https://storage.googleapis.com/ai-voice-prod-storage/platform/c37e784d-25b1-403b-a4a1-34dc6debc145/voices/2025/04/13/be119c37-225c-4e2c-8a0e-6301a751a45e/uploaded-audio.mp3?GoogleAccessId=ai-voice-api-prod-sa%40algomatic-global-ai-voice.iam.gserviceaccount.com&Expires=1744608807&Signature=mhiyIsFU5%2F0f0uoIRVIWynPVhn1mcaeYWO5m6QlELfhN6WhgsuPXjZy9bv5T%2By0Nhu9dzeIFehxX5UEdCKzxlbc3LqA5lNfs2Kx5u5pQgx3M8%2FHb%2BKRK4Luz4GI8t2ck%2By5q%2FE9GTpQxnXcd5XA0fIc2eFsPfZdhmwEowg5lpL%2Br16u%2BWokYk38ibqcDaHn9M3%2B4ANfWhnUaeWIvJGfH4F8swaf1vWKhecTrvRybk%2FustxRU8gv14vNHWIE93JUj7T6KNscTXtEK3WAgqaAPo5oUbe7qgcQe4ysd5ALAKxowpijKUJj%2BNb2InfMAZo04cvOhCKCwzG1CzZhlmuydaw%3D%3D',
            format="audio/mp3",
            loop=False
        )
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