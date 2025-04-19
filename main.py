import os   #.envから環境設定変数を取得するために必要
import base64
from dotenv import load_dotenv  #.envファイルの読み込みに必要なモジュール
import streamlit as st  #streamlitの使用に必要
from supabase import create_client, Client
from elevenlabs import ElevenLabs, play #ElevenLabs APIの利用に必要
from io import BytesIO  #ElevenLabsで作成した合成音声をバイト型に変換

#環境変数の読み込み
load_dotenv()

#ページ設定を行う。サイトのタイトルやアイコン、画面幅を設定する
#おそらくファイルの一番初めに記載しておかないといけないみたい
st.set_page_config(
        page_title="おはなしたからばこ",
        page_icon="📕",
        layout="wide",
    )

#ページ遷移用の関数
def go_to_page(page_name):
    st.session_state.page = page_name

# Supabaseクライアントの初期化
def get_supabase_client():
    url: str = os.environ.get("SUPABASE_URL")
    key: str = os.environ.get("SUPABASE_KEY")
    supabase: Client = create_client(url, key)
    return supabase

def sign_up(email: str, password: str):
    """ユーザー登録"""
    supabase = get_supabase_client()
    return supabase.auth.sign_up({"email": email, "password": password})

def sign_in(email: str, password: str):
    """ログイン"""
    supabase = get_supabase_client()
    return supabase.auth.sign_in_with_password({"email": email, "password": password})

def sign_out():
    """ログアウト"""
    supabase = get_supabase_client()
    supabase.auth.sign_out()
    st.session_state.clear()

def check_auth():
    """認証状態のチェック"""
    return 'user' in st.session_state

def login_signup_page():
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
        div[data-baseweb="input"] input {
            background-color: white !important;
        }
        </style>
        """,
        unsafe_allow_html=True
    )
    
    with st.container(border=False):
        st.image('./picture/app_logo.png')
        st.container(height=10, border=False)

    #ログイン/サインアップページの表示
    st.header("ログイン/サインアップ")
    tab1, tab2 = st.tabs(["ログイン", "サインアップ"])

    with tab1:
        email = st.text_input("メールアドレス", key="login_email")
        password = st.text_input("パスワード", type="password", key="login_password")
        if st.button("ログイン"):
            try:
                res = sign_in(email, password)
                st.session_state.user = res.user
                st.success("ログインに成功しました")
                st.session_state.page = "main_page"
                st.rerun()
            except Exception as e:
                st.error(f"ログインに失敗しました: {str(e)}")
    
    with tab2:
        new_email = st.text_input("メールアドレス", key="signup_email")
        new_password = st.text_input("パスワード", type="password", key="signup_password")
        if st.button("サインアップ"):
            try:
                res = sign_up(new_email, new_password)
                st.success("アカウントが作成されました。メールを確認してアカウントを有効化してください。")
            except Exception as e:
                st.error(f"サインアップに失敗しました: {str(e)}")

def main_page():
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

    with st.container(border=False):
        st.image('./picture/app_logo.png')
        st.container(height=10, border=False)
    
    with st.container(border=False):
        st.markdown(
        """
        <div style='text-align: center; color:#634320;'>
            <h2>どうやって絵本（えほん）をつくる？</h2>
        </div>
        """,
        unsafe_allow_html=True
        )

    with st.container(border=False):
        left, center, right = st.columns([1, 3, 1], vertical_alignment="center")
        with center:
            st.container(height=40, border=False)
            st.markdown("""
                <a href="/input" target="_self">
                    <button style='font-size:18px; padding:0.5em 1em; border-radius:8px; background-color:#4CAF50; color:white; border:none; width:100%;'>
                        📖 すきな絵本（えほん）をつくる
                    </button>
                </a>
            """, unsafe_allow_html=True)
            st.container(height=20, border=False)
            st.markdown("""
                <a href="/book_list" target="_self">
                    <button style='font-size:18px; padding:0.5em 1em; border-radius:8px; background-color:#4CAF50; color:white; border:none; width:100%;'>
                        📖 むかしの本（ほん）からつくる
                    </button>
                </a>
            """, unsafe_allow_html=True)
            st.container(height=40, border=False)

    with st.container(border=False):
        cols = st.columns(3, vertical_alignment="center")
        with cols[1]:
            if st.button("ログアウト", use_container_width=True):
                sign_out()
                st.rerun()

def main():
    """アプリケーションのメイン処理"""
    if not check_auth():
        login_signup_page()
    else: main_page()

if __name__ == "__main__":
    #main()
    main_page()