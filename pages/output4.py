import streamlit as st
# from elevenlabs import ElevenLabs, play #ElevenLabs APIの利用に必要
# from io import BytesIO  #ElevenLabsで作成した合成音声をバイト型に変換
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
        st.switch_page("pages/output3.py")  # pages/output2.py に遷移する

with st.container():
    #画像を挿入したい時に使う
    #変換から画像を取得して下記URLに格納する
    st.image("./output/3.jpeg")

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

    #変数カラ下記のURLに該当する情報を当てはめる
    st.audio(
        "./output/voice3.mp3",
        format="audio/mp3",
        loop=False
    )
    #エキスパンダーでテキストを表示
    #変数から取得したテキストを表示する
    expander = st.expander("テキストを表示")
    expander.write(st.session_state.audio_text[3])

#ダウンロード機能の組み込み
st.download_button(
    label="Download Image",
    data="",
    file_name='book.jpg',
    icon=":material/download:"
)

#フィードバック機能の組み込み
sentiment_mapping = ["one", "two", "three", "four", "five"]
selected = st.feedback("stars")

#保存するボタンがある

#セッションステートにフィードバックの点数をアペンドする
#候補→ID,名前、性別、物語のテイスト、画風、なりたい職業、フィードバックの点数、起承転結別のテキスト情報、だった気がする
#いけるなら画像を保存する

#supabase上に保存するコードを実行する
# 保存ボタン
if st.button("保存", key="save_story_button"):
    try:
        success = save_story(user_id, title, story0, story1, story2, story3)
        if success:
            st.success("ストーリーを保存しました！")
            st.rerun()
        else:
            st.error("ストーリーの保存に失敗しました。")
    except Exception as e:
        st.error(f"エラーが発生しました: {str(e)}")