import streamlit as st
from dotenv import load_dotenv  #.envファイルの読み込みに必要なモジュール
import requests
import os   #.envから環境設定変数を取得するために必要

from openai import OpenAI
import json
from yochanchanco import make_story_gpt, make_image_prompt_gpt, concat_image_prompt, make_image_stability

#ページ設定を行う。サイトのタイトルやアイコン、画面幅を設定する
#おそらくファイルの一番初めに記載しておかないといけないみたい
st.set_page_config(
        page_title="おはなしたからばこ",
        page_icon="📕",
        layout="wide",
    )

#初期化(session_stateのセット)
#空欄だとエラーが起きるので、初期値をセットしておく
if "gender" not in st.session_state:
    st.session_state.gender = "男の子"

#ページ遷移用の関数
# def go_to_page(page_name):
#     st.session_state.page = page_name

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

#containerの枠線を消す
st.markdown("""
<style>
    div[data-testid="stVerticalBlock"] > div {
        border: none !important;
        box-shadow: none !important;
    }
</style>
""", unsafe_allow_html=True)

#名前の入力(st.session_state.name)
#空欄だとエラーが起きるので、初期値をセットしておく
with st.container():
    st.markdown(" <div style='text-align: center; color:#634320;'><h5>すきな名前（なまえ）をかいてね</h5></div>", unsafe_allow_html=True)
    st.text_input(label="", value="テックちゃん", placeholder="名前をいれてね", key="name", label_visibility="collapsed")

#登場人物の選択(st.session_state.gender)
genders = ["男（おとこ）の子", "女（おんな）の子"]  
with st.container():
    st.markdown(" <div style='text-align: center; color:#634320;'><h5>男の子と女の子どっちにする？</h5></div>", unsafe_allow_html=True)
    cols = st.columns(len(genders))
    for i, gender in enumerate(genders):
        with cols[i]:
            if st.button(gender, use_container_width=True):
                st.session_state.gender = gender
    st.container(height=5)

#ジョブの選択(st.session_state.job)
job_options = []
if st.session_state.gender == "男（おとこ）の子":
    job_options.extend(["魔法使い", "勇者", "王子様", "海賊"])
elif st.session_state.gender == "女（おんな）の子":
    job_options.extend(["魔法使い", "お姫様", "アイドル"])
with st.container():
    st.markdown(" <div style='text-align: center; color:#634320;'><h5>どんなお仕事（しごと）をしてみる？</h5></div>", unsafe_allow_html=True)
    input_job = st.selectbox(label="", options=job_options, label_visibility="collapsed")
    st.session_state.job = input_job

#どんな絵本にするか選択(st.session_state.theme)
themes = ["ふしぎ", "びっくり", "うれしい"]
with st.container():
    st.markdown(" <div style='text-align: center; color:#634320;'><h5>どんな絵本（えほん）にする？</h5></div>", unsafe_allow_html=True)
    cols = st.columns(len(themes))
    for i, theme in enumerate(themes):
        with cols[i]:
            if st.button(theme, use_container_width=True):
                st.session_state.theme = theme

#イラストの画風を選択(st.session_state.preset)
preset_options = [
    {"id" : "enhance", "label" : "バランス"},
    {"id" : "anime", "label" : "アニメ"},
    {"id" : "origami", "label" : "おりがみ"}
]
with st.container():
    st.markdown(" <div style='text-align: center; color:#634320;'><h5>どんなイラストで絵本（えほん）をつくる？</h5></div>", unsafe_allow_html=True)
    cols = st.columns(len(preset_options))
    for i, preset_option in enumerate(preset_options):
        with cols[i]:
            if st.button(preset_option["label"], use_container_width=True):
                st.session_state.preset = preset_option["id"]
    st.container(height=5)

#音声の選択(st.session_state.voice)
voice_options = [
    {"id" : "b6142f17-1e4b-4fa3-9975-61c2ae186e46", "data" : {"label" : "かっこいい", "audio" : 'https://storage.googleapis.com/ai-voice-prod-storage/platform/c37e784d-25b1-403b-a4a1-34dc6debc145/voices/2025/04/17/4a332af1-0585-4d1a-aff4-99752bdba9ab/uploaded-audio.mp3?GoogleAccessId=ai-voice-api-prod-sa%40algomatic-global-ai-voice.iam.gserviceaccount.com&Expires=1744979166&Signature=TNi9t7v053FJYr8SJgzwcDXnWeWDwShv8yVTv%2FLid26Iepym32pwvui1VMQkdbgPmjsC0ilkq6FJ5pgF7NUSgnMRsHDUNbcNdU4ZdMFNr8k%2FF73cQxAWylca5cQke%2BLcwhQSpip7fxlWrgiBs3JFv9HarytE%2FGHOrNj9ip3XMdh8PaokDswALq%2BeL9chw8ELo6jEOoMuHzYo%2BCGrqnmjnbJ3WJhxVXj9h0oM0HrAXXpHgeX4Z7SJskeqsuV5vNejICbpOZAtfIszlqsf%2BvTmIvQK1FUdBXetC98wal9%2FeqM5UeVJv6t4YTOpl%2BPT0nbQvIPzOEgk2HRQcYCRGjeiSg%3D%3D'}},
    {"id" : "d158278c-c4fa-461a-b271-468146ad51c9", "data" : {"label" : "かわいい", "audio" : 'https://storage.googleapis.com/ai-voice-prod-storage/platform/c37e784d-25b1-403b-a4a1-34dc6debc145/voices/2025/04/17/77883ffa-8181-4d46-b688-20178087c3ac/uploaded-audio.mp3?GoogleAccessId=ai-voice-api-prod-sa%40algomatic-global-ai-voice.iam.gserviceaccount.com&Expires=1744979195&Signature=PzN4eYH4KgNuiJVW7zfjogMlrkKzSa9V2Oen8jzE%2FNDr1zim29BEEuoVg2qlZUTmMSj%2BNe2J1LrDis29D%2FnWd%2FcVIzdNK%2BV1DlU1CBJI2nCKAHubDuCDX6LBtIdg9AQJBzyj7mAUsVND%2BHRQJWrq0rgPh5xU%2F8SvhAzhw3kS%2FepNNqAvvmSGBmbGlDkzugpyy7biSmWo5rLLdLdkkNrrhGt1XC1JNtbpXVcu0UGZfMiPw7tcqt4N69MGRIKsjKndosSyiOjk2xiM4F%2FdGoJanKwzzR%2BXKmnF0aorQ5%2BbbW1M7EC%2Fy3UWIx0sdNNkbBveTHTYFe3fFNVL6HD95ZTjjQ%3D%3D'}},
    {"id" : "2773f3eb-2d5e-452b-b626-59d0869c53ec", "data" : {"label" : "サンタクロース", "audio" : 'https://storage.googleapis.com/ai-voice-prod-storage/platform/c37e784d-25b1-403b-a4a1-34dc6debc145/voices/2025/04/17/01f95aa6-8df6-405e-b4a1-807bed3e3822/uploaded-audio.mp3?GoogleAccessId=ai-voice-api-prod-sa%40algomatic-global-ai-voice.iam.gserviceaccount.com&Expires=1744979219&Signature=ZiiSCc6rrd0HuIL8ULxSbpgpUBJbqrdc54Jubly5j7OeYQAQmwBpgKHacD0%2FnoevEYVWqWlXgYzUpa6GMesxTDEgcXU0W6FV4ZZaLg3MEw4hArnPRRhS9jvl4KfMd7tr4YWGov6yroHXIviIrciK7coqoWvwyPyQrWw4hl4aXUb2IiOKBVkvercdSM6WahuS7Wm0fo6ph3DLdaDzWzXNxSFJ13FPOI2giZK%2B33QEJrL1mqgOhyUZSV%2FGnfcH7bcNHyYCh85LLGtn1RYW8hYIPl5LwUd040MrSJ7is8FNVAHnZFor7LC0q3kk%2BHlx1HArUcyvbF1gZuqfGBtLY2FWtg%3D%3D'}},
]
with st.container():
    st.markdown(" <div style='text-align: center; color:#634320;'><h5>どんな声がいい？</h5></div>", unsafe_allow_html=True)
    #カード表示
    cols = st.columns(len(voice_options))
    voice_selected = None
    for i, voice_option in enumerate(voice_options):
        with cols[i]:
            if st.button(voice_option["data"]["label"], use_container_width=True):
                st.session_state.voice = voice_option["id"]
            st.write("試しに聞いてみる")
            st.audio(
                voice_options[i]["data"]["audio"],
                format="audio/mp3",
                loop=False
            )
    st.container(height=3)

#st.なんとかに全部のセッション情報をいれておく
#st.session_state.all = {

#物語を作るためのボタン
# st.markdown("""
#                 <a href="/output1" target="_self">
#                     <button style='font-size:18px; padding:0.5em 1em; border-radius:8px; background-color:#4CAF50; color:white; border:none; width:100%;'>
#                         📖 準備ができたので読みに行く
#                     </button>
#                 </a>
#             """, unsafe_allow_html=True)

#ストーリーの作成するコードの実行
gpted_story = make_story_gpt(st.session_state.gender, st.session_state.job, st.session_state.theme)
gpted_prompt_parts = make_image_prompt_gpt(gpted_story)
merged_listed_prompts = concat_image_prompt(gpted_prompt_parts)
page = 0 # このハードコーディングは残す
make_image_stability(merged_listed_prompts, st.session_state.preset, page)

#４枚分の画像生成するためのプロンプトを生成するコードの実行（辞書型になってる）
#セッション情報にアペンドする

#特定の変数に今のページがどこかを記載しておく
#page = 0が欲しい#→ハードコーディング
#1枚目の画像を作るコードの実行
#これがGitHubのoutputフォルダに入るイメージ
#0.jpgが保存される

#1枚目のストーリーを読むにじボイスのAPIで音声を作成するコードの実行
#これがGitHubのoutputフォルダに入るイメージ
#0.mp3が保存される

#↓これはページの切り替えの動作のトリガーにする
st.markdown("""
                <a href="/output1" target="_self">
                    <button style='font-size:18px; padding:0.5em 1em; border-radius:8px; background-color:#4CAF50; color:white; border:none; width:100%;'>
                        📖 準備ができたので読みに行く
                    </button>
                </a>
            """, unsafe_allow_html=True)

    