import streamlit as st
from dotenv import load_dotenv  #.envファイルの読み込みに必要なモジュール
from streamlit_extras.switch_page_button import switch_page
import requests
import os   #.envから環境設定変数を取得するために必要
from openai import OpenAI
import json
import yochanchanco as yochan
from voice import voice_generated as vg


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
    input_name = st.text_input(label="", value="テックちゃん", placeholder="名前をいれてね", label_visibility="collapsed")
    st.session_state.name = input_name

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
    {"id" : "b6142f17-1e4b-4fa3-9975-61c2ae186e46", "data" : {"label" : "かっこいい", "audio" : "voicesample/sample1.mp3"}},
    {"id" : "d158278c-c4fa-461a-b271-468146ad51c9", "data" : {"label" : "かわいい", "audio" : "voicesample/sample2.mp3"}},
    {"id" : "2773f3eb-2d5e-452b-b626-59d0869c53ec", "data" : {"label" : "サンタクロース", "audio" : "voicesample/sample3.mp3"}},
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


#物語を作るためのボタン
if st.button("📖 絵本（えほん）をつくる", use_container_width=True):
    gpted_story = yochan.make_story_gpt(st.session_state.gender, st.session_state.job, st.session_state.theme)
    gpted_audio_text = yochan.make_audio_text_gpt(gpted_story)
    st.session_state.audio_text = gpted_audio_text
    gpted_prompt_parts = yochan.make_image_prompt_gpt(gpted_story)
    merged_listed_prompts = yochan.concat_image_prompt(gpted_prompt_parts)
    page = 0 # ハードコーディングでok
    yochan.make_image_stability(merged_listed_prompts, st.session_state.preset, page)
    st.session_state.story = merged_listed_prompts

    #これがGitHubのoutputフォルダに入るイメージ←githubへの入れ方分からなかった。streamlitクラウドに期待
    #0.jpegが保存される

    #1枚目のストーリーを読むにじボイスのAPIで音声を作成するコードの実行
    #これがGitHubのoutputフォルダに入るイメージ
    #0.mp3が保存される
    vg(st.session_state.voice, st.session_state.audio_text, page)
    
    #st.なんとかに全部のセッション情報をいれておく
    #st.session_state.all = {

    #↓これはページの切り替えの動作のトリガーにする
if st.button("📖 準備ができたので読みに行く", use_container_width=True):
    st.switch_page("pages/output1.py")  # pages/output1.py に遷移する
    