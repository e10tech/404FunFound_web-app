import os
from supabase import create_client, Client
from dotenv import load_dotenv
import uuid

# 環境変数の読み込み
load_dotenv()

# Supabaseクライアントの初期化
supabase: Client = create_client(
    os.environ.get("SUPABASE_URL"),
    os.environ.get("SUPABASE_KEY")
)

def save_story(user_id: str, title: str, character_name: str, gender: str, job: str, theme: str, story_texts: dict) -> dict:
    """
    ストーリーをデータベースに保存する関数
    
    Args:
        user_id (str): ユーザーID
        title (str): 物語のタイトル
        character_name (str): キャラクター名
        gender (str): 性別
        job (str): 職業
        theme (str): テーマ
        story_texts (dict): ストーリーテキスト {0: "text0", 1: "text1", 2: "text2", 3: "text3"}
    
    Returns:
        dict: 保存されたストーリーのデータ
    """
    try:
        # Auth0のユーザーIDから'auth0|'プレフィックスを削除
        cleaned_user_id = user_id.replace('auth0|', '') if user_id.startswith('auth0|') else user_id
        
        # UUIDの生成
        story_uuid = uuid.uuid4()
        
        # ストーリーデータの準備
        story_data = {
            'id': str(story_uuid),
            'user_id': cleaned_user_id,
            'title': title,
            'character_name': character_name,
            'character_gender': gender,
            'character_job': job,
            'theme': theme,
            'story0': story_texts[0],
            'story1': story_texts[1],
            'story2': story_texts[2],
            'story3': story_texts[3]
        }
        
        # データベースに保存
        response = supabase.table('stories').insert(story_data).execute()
        
        if not response.data:
            raise Exception("ストーリーデータの保存に失敗しました")
            
        return response.data[0]
        
    except Exception as e:
        raise Exception(f"ストーリーの保存に失敗しました: {str(e)}")

def get_all_stories() -> list:
    """
    保存された全てのストーリーを取得する関数
    
    Returns:
        list: 保存されているストーリーのリスト
    """
    try:
        response = supabase.table('stories').select("*").order('created_at', desc=True).execute()
        return response.data
    except Exception as e:
        print(f"Error fetching stories: {e}")
        return [] 