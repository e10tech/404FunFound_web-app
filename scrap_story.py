"""
共通で読み込む処理
一応環境変数もここで読み込むようにしている
"""

#各種ライブラリのインポート
from openai import OpenAI
import os
import sys
import json
from dotenv import load_dotenv
import requests
import streamlit as st
import pandas as pd

#環境変数の読み込み
load_dotenv()

#APIキーの取得→openaiのAPIキー
openai_api_key = os.getenv('OPENAI_API_KEY')
if openai_api_key is None:
    print("Error: OPENAI_API_KEY is not set in the environment variables.")
    sys.exit(1)

#APIキーの取得→stable diffusionのAPIキー
stability_api_key = os.getenv('STABILITY_API_KEY')
if stability_api_key is None:
    print("Error: STABILITY_API_KEY is not set in the environment variables.")
    sys.exit(1)

#APIキーの取得→にじボイスのAPIキー
x_api_key = os.getenv('x_api_key')
if x_api_key is None:
    print("Error: X_API_KEY is not set in the environment variables.")
    sys.exit(1)



"""
起承転結のストーリーを生成する関数。
chapter_text: 対象となるチャプターの本文（1万字程度）
openai_api_key: OpenAI APIキー
return: ストーリーを辞書形式で返す（起・承・転・結・原作）
ここはトークンの消費でかいのでやりすぎないように注意
storyという辞書型の変数もoutput.pyに必要→そこにreturnする
"""
#ここで重要なのはchapter_textという変数にcsvファイルから読み込んだチャプターの本文を入れること。
def make_story(chapter_text: str, openai_api_key: str) -> list:
    # OpenAI APIはすでにインポートされているはず
    #openai_api_key = os.getenv("OPENAI_API_KEY")
    client = OpenAI(api_key=openai_api_key)

    #GPTへのリクエスト
    response = client.responses.create(
        model="gpt-4o-mini",  # コスパ重視モデル！精度欲しいならgpt-4.1でもOK
        input=[
            {
                "role": "system",
                "content": "あなたはプロフェッショナルな3歳児向けの絵本作家です。"
            },
            {
                "role": "user",
                "content": (
                    "以下の長文は、ある物語の1チャプターに相当する内容です。この内容をもとに、\n"
                    "3歳児〜低学年でも理解できるように、やさしい言葉で起承転結の絵本風ストーリーに要約してください。\n"
                    "・起承転結それぞれの分量は100〜180文字が理想です。\n"
                    "・低学年でも読めるようにすべてひらがなで出力してください。\n"
                    "・原作部分は漢字を入れて大丈夫です\n"
                    "・原作はテキストデータから推察して設定してください。\n"
                    "・出力はJSONの構造のみで、```で囲んだりせず、そのまま返してください。\n"
                    "・以下のような形式を参考にしてください：\n"
                    "{\n"
                    "  \"起\": \"あるひ、ありすはおねえさんとかわべにすわっていました。たいくつしていたら、ふくをきたしろいうさぎが「ちこくちこく！」といいながらはしっていきました。\",\n"
                    "  \"承\": \"ありすはうさぎをおいかけて、あなにとびこみました。ながいながいあなをおちていくと、ふしぎなへやにたどりつきました。\",\n"
                    "  \"転\": \"へやにはちいさなとびらがありました。ありすは「のんで」とかかれたびんのなかみをのむと、からだがちいさくなりましたちいさくなったありすは、とびらをとおって、きれいなおにわにむかいました。ふしぎなぼうけんのはじまりです。\",\n"
                    "  \"結\": \"さいごにはげんきにむらへかえり、みんなにえがおがひろがりました。\",\n"
                    "  \"原作\": \"不思議の国のアリス\"\n"
                    "}\n"
                    "出力は日本語でお願いします。\n"
                    "【チャプター本文】：\n"
                    f"{chapter_text}\n"
                )
            }
        ]
    )
    #json形式かバリデーションするエラーハンドリング
    try:
        story = json.loads(response.output_text)
        required_keys = ["起", "承", "転", "結", "原作"]
        if all(key in story for key in required_keys):
            st.write("ストーリーが正しく生成されました。")
        else:
            st.write("ストーリーに必要なキーが不足しています。")

    except json.JSONDecodeError as e:
        st.write("JSONのデコードに失敗しました。")
        st.write(f"エラー内容: {e}")

    #全てエラーがなければ、ストーリーを返す
    #辞書型にデータを追加する場合は、story['起']のようにして追加する
    story.update({
        "起": story["起"],
        "承": story["承"],
        "転": story["転"],
        "結": story["結"],
        "原作": story["原作"]
    })
    story = [story['起'], story['承'], story['転'], story['結']]
    return story
    #ストリームリット実装時はst.set_state(story=story)に保存して残す
    #このstoryを変数にいれて他のpythonファイルが実行するときも残るようにする



"""
画像生成AIの個別に受け渡すプロンプトを生成する関数
起承転結一気につくりリストに格納する
"""
#ここで重要なのはstoryという変数からstory[起]を抽出し受け渡すこと
def make_image_prompt_gpt(story: list, openai_api_key: str) -> list:
    # OpenAI APIはすでにインポートされているはず
    #openai_api_key = os.getenv("OPENAI_API_KEY")
    client = OpenAI(api_key=openai_api_key)

    # GPTへのリクエスト
    response = client.responses.create(
        model="gpt-4o-mini",  # コスパ重視モデル！精度欲しいならgpt-4.1でもOK
        input=[
            {
                "role": "system",
                "content": "あなたはStable Diffusion3.5で３歳～５歳用の絵本に相応しいイラストをつくるプロフェッショナルです。"
            },
            {
                "role": "user",
                "content": (
                    "以下の【story】をベースにして、英語で、画像生成プロンプトのパーツを作成してください。【画像生成プロンプトの注意事項】は必ず順守してください。json形式で出力してください\n"
                    "\n"
                    "【story】\n"
                    f"{story}\n"
                    "以下は、3歳〜低学年向け絵本の1シーンに相当するストーリーです\n"
                    "ストーリーをもとに、Stability AIで折紙風の絵本のやさしいイラストを生成するためのプロンプトを考えてください\n"
                    "4つのページにをそれぞれの[story]のリスト型に相応しいプロンプトを順につくりリスト型の英語表記プロンプトに組み換え\n"
                    "出力の過程で改行やよけいなダブルコーテーションは不要で指定した出力形式の型にしてください\n"
                    "条件：\n"
                    "・出力形式はリスト型"
                    "・画風は「明るくかわいらしい折り紙風」\n"
                    "・主人公がどういう姿かも補足してください\n"
                    "・プロンプトは英語で書いてください\n"
                    "・ファンタジーすぎず、子供が見て安心できるイメージにしてください\n"
                    "・主人公の髪色、目の色、服、年齢のプロンプトは全てのリストで統一し必ず最初の方に記載してください\n"
                    "・以下のような形式を参考にしてください：\n"
                    "出力形式（例）：\n"
                    f"[\"Prompt 1\", \"Prompt 2\", \"Prompt 3\", \"Prompt 4\"]\n"
                )
            }
        ]
    )
    #前処理
    response_text = response.output_text.strip()
    # もしバッククォートで囲まれてたら取り除く
    if response_text.startswith("```json"):
        response_text = response_text.replace("```json", "").replace("```", "").strip()

    # 出力された文字列をPythonのリストに変換
    try:
        image_prompts = json.loads(response_text)
        if len(image_prompts) != 4:
            st.warning("プロンプトの数が4個じゃなかったよ！")
            st.write(image_prompts)
    except json.JSONDecodeError as e:
        st.error("プロンプトのJSONデコードに失敗しました😢")
        st.code(response_text)
        return []

    return image_prompts
    #これをsession_stateに格納して保存されるようにする



"""
画像生成を行う関数
ここで重要なのはimage_promptsから必要なプロンプトを抜き出すこと
now_pageはページ数を指定する変数→output(x)_scrapのコードに記載が必要
"""

def generate_image(image_prompts: list, now_page: int):
    stability_api_key = os.getenv("STABILITY_API_KEY")
    # image_promptは、上のコードからinputされたものを使えるように変更する。
    base_prompt = "masterpiece, best quality, ultra detailed, watercolor style, soft pastel palette,origami, gentle lighting,"
    image_prompt = image_prompts[now_page]  # 1ページ目のプロンプトを取得

    response = requests.post(
        f"https://api.stability.ai/v2beta/stable-image/generate/sd3",
        headers={
            "authorization": f"Bearer {stability_api_key}",
            "accept": "image/*"
        },
        files={"none": ''},
        data={
            "model": "sd3.5-large-turbo", # sd3.5-large, sd3.5-large-turbo, sd3.5-medium から選ぶ
            "output_format": "jpeg",
            "prompt": base_prompt + image_prompt,
            "negative_prompt": "realistic photo, cluttered, grotesque, deformed hands, extra limbs, text, watermark",
            "style_preset": "origami",#とりあえず一旦origami固定でやってみる
        },
    )

    if response.status_code == 200:
        # 出力ファイルのパスを作成（例：./output/1.jpeg）
        output_path = f"./output/{now_page}.jpeg"
        # 出力フォルダ（./output）が存在しない場合は作成
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        # 取得した画像データをバイナリ形式でファイルに保存
        with open(output_path, 'wb') as file:
            file.write(response.content)
        # 保存した画像のファイルパスを返す（後で表示や処理に使える！）
        return output_path
    else:
        # エラーが返ってきた場合は例外を発生させて詳細を表示（API側のエラー内容が見れる！）
        raise Exception(str(response.json()))




























"""
起のストーリー用の画像生成プロンプトを生成する関数。
image_prompt_1という変数に文字列が格納される。
output1_scrapにimage_promptsというリストが必要
"""
#ここで重要なのはstoryという変数からstory[起]を抽出し受け渡すこと
def make_prompt_1(story: dict, openai_api_key: str, image_prompts) -> str:
    # OpenAI APIはすでにインポートされているはず
    #openai_api_key = os.getenv("OPENAI_API_KEY")
    client = OpenAI(api_key=openai_api_key)

    # GPTへのリクエスト
    response = client.responses.create(
        model="gpt-4o-mini",  # コスパ重視モデル！精度欲しいならgpt-4.1でもOK
        input=[
            {
                "role": "system",
                "content": "あなたはStable Diffusion3.5で３歳～５歳用の絵本に相応しいイラストをつくるプロフェッショナルです。"
            },
            {
                "role": "user",
                "content": (
                    "以下は、3歳〜低学年向け絵本の1シーンに相当するストーリーです\n"
                    "ストーリーをもとに、Stability AIで絵本風のやさしいイラストを生成するためのプロンプトを考えてください\n"
                    "条件：\n"
                    "・画風は「明るくかわいらしい絵本風」\n"
                    "・主人公がどういう姿かも補足してください\n"
                    "・プロンプトは英語で書いてください\n"
                    "・ファンタジーすぎず、子供が見て安心できるイメージにしてください\n"
                    "・アートスタイルは「storybook illustration」\n"
                    "・髪色、目の色、服、年齢のプロンプトは必ず最初の方に記載してください\n"
                    "・以下のような形式を参考にしてください：\n"
                    "出力形式（例）：\n"
                    "a young girl with blonde hair wearing a blue dress, smiling in a flower garden, soft pastel colors, storybook illustration, children's picture book style, wide view, gentle lighting"
                    "プロンプトをこの形式だけで返してください。\n"
                    f"【ストーリー】：\n{story['起']}\n"
                )
            }
        ]
    )
    # 画像生成に受け渡すためのプロンプトをimage_prompt_1に格納
    #ストリームリット実装時はst.set_state(～～～)に格納する
    image_prompt = response.output_text
    image_prompts.append(image_prompt)  # image_prompt_1をリストに追加
    return image_prompts
    #これをsession_stateに格納して保存されるようにする



"""
承のストーリー用の画像生成プロンプトを生成する関数。
「起」に追加して見た目情報の継承もプロンプトとして入れておく
image_promptsというリストに新たに格納される。
"""
#ここで重要なのはstoryという変数からstory[起]を抽出し受け渡すこと
def make_prompt_2(story: dict, openai_api_key: str, image_prompts) -> str:
    # OpenAI APIはすでにインポートされているはず
    #openai_api_key = os.getenv("OPENAI_API_KEY")
    client = OpenAI(api_key=openai_api_key)

    # GPTへのリクエスト
    response = client.responses.create(
        model="gpt-4o-mini",  # コスパ重視モデル！精度欲しいならgpt-4.1でもOK
        input=[
            {
                "role": "system",
                "content": "あなたはStable Diffusion3.5で３歳～５歳用の絵本に相応しいイラストをつくるプロフェッショナルです。"
            },
            {
                "role": "user",
                "content": (
                    "以下は、3歳〜低学年向け絵本の1シーンに相当するストーリーです\n"
                    "前ページでは下記の画像生成プロンプトを使用しました。登場キャラクターの髪型や服装などビジュアル情報は引き継いでください。\n"
                    f"前ページプロンプト：\n{image_prompts[0]}\n"
                    "ストーリーをもとに、Stability AIで絵本風のやさしいイラストを生成するためのプロンプトを考えてください\n"
                    "条件：\n"
                    "・画風は「明るくかわいらしい絵本風」\n"
                    "・主人公がどういう姿かも補足してください\n"
                    "・プロンプトは英語で書いてください\n"
                    "・ファンタジーすぎず、子供が見て安心できるイメージにしてください\n"
                    "・アートスタイルは「storybook illustration」\n"
                    "・髪色、目の色、服、年齢のプロンプトは必ず最初の方に記載してください\n"
                    "・以下のような形式を参考にしてください：\n"
                    "出力形式（例）：\n"
                    "a young girl with blonde hair wearing a blue dress, smiling in a flower garden, soft pastel colors, storybook illustration, children's picture book style, wide view, gentle lighting"
                    "プロンプトをこの形式だけで返してください。\n"
                    f"【ストーリー】：\n{story['承']}\n"
                )
            }
        ]
    )
    # 画像生成に受け渡すためのプロンプトをimage_prompt_2に格納
    #ストリームリット実装時はst.set_state(～～～)に格納する
    image_prompt = response.output_text
    image_prompts.append(image_prompt)  # image_prompt_2をリストに追加
    return image_prompts
    #これをsession_stateに格納して保存されるようにする



"""
転のストーリー用の画像生成プロンプトを生成する関数。
image_promptsというリストに新たに格納される。
"""
#ここで重要なのはstoryという変数からstory[起]を抽出し受け渡すこと
def make_prompt_3(story: dict, openai_api_key: str, image_prompts: list) -> str:
    # OpenAI APIはすでにインポートされているはず
    #openai_api_key = os.getenv("OPENAI_API_KEY")
    client = OpenAI(api_key=openai_api_key)

    # GPTへのリクエスト
    response = client.responses.create(
        model="gpt-4o-mini",  # コスパ重視モデル！精度欲しいならgpt-4.1でもOK
        input=[
            {
                "role": "system",
                "content": "あなたはStable Diffusion3.5で３歳～５歳用の絵本に相応しいイラストをつくるプロフェッショナルです。"
            },
            {
                "role": "user",
                "content": (
                    "以下は、3歳〜低学年向け絵本の1シーンに相当するストーリーです\n"
                    "前ページでは下記の画像生成プロンプトを使用しました。登場キャラクターの髪型や服装などビジュアル情報は引き継いでください。\n"
                    f"前ページプロンプト：\n{image_prompts[1]}\n"
                    "ストーリーをもとに、Stability AIで絵本風のやさしいイラストを生成するためのプロンプトを考えてください\n"
                    "条件：\n"
                    "・画風は「明るくかわいらしい絵本風」\n"
                    "・主人公がどういう姿かも補足してください\n"
                    "・プロンプトは英語で書いてください\n"
                    "・ファンタジーすぎず、子供が見て安心できるイメージにしてください\n"
                    "・アートスタイルは「storybook illustration」\n"
                    "・髪色、目の色、服、年齢のプロンプトは必ず最初の方に記載してください\n"
                    "・以下のような形式を参考にしてください：\n"
                    "出力形式（例）：\n"
                    "a young girl with blonde hair wearing a blue dress, smiling in a flower garden, soft pastel colors, storybook illustration, children's picture book style, wide view, gentle lighting"
                    "プロンプトをこの形式だけで返してください。\n"
                    f"【ストーリー】：\n{story['転']}\n"
                )
            }
        ]
    )
    # 画像生成に受け渡すためのプロンプトをimage_prompt_2に格納
    #ストリームリット実装時はst.set_state(～～～)に格納する
    image_prompt = response.output_text
    image_prompts.append(image_prompt)  # image_prompt_3をリストに追加
    return image_prompts
    #これをsession_stateに格納して保存されるようにする


"""
結のストーリー用の画像生成プロンプトを生成する関数。
image_promptsというリストに新たに格納される。
"""
#ここで重要なのはstoryという変数からstory[起]を抽出し受け渡すこと
def make_prompt_4(story: dict, openai_api_key: str, image_prompts: list) -> str:
    # OpenAI APIはすでにインポートされているはず
    #openai_api_key = os.getenv("OPENAI_API_KEY")
    client = OpenAI(api_key=openai_api_key)

    # GPTへのリクエスト
    response = client.responses.create(
        model="gpt-4o-mini",  # コスパ重視モデル！精度欲しいならgpt-4.1でもOK
        input=[
            {
                "role": "system",
                "content": "あなたはStable Diffusion3.5で３歳～５歳用の絵本に相応しいイラストをつくるプロフェッショナルです。"
            },
            {
                "role": "user",
                "content": (
                    "以下は、3歳〜低学年向け絵本の1シーンに相当するストーリーです\n"
                    "前ページでは下記の画像生成プロンプトを使用しました。登場キャラクターの髪型や服装などビジュアル情報は引き継いでください。\n"
                    f"前ページプロンプト：\n{image_prompts[2]}\n"
                    "ストーリーをもとに、Stability AIで絵本風のやさしいイラストを生成するためのプロンプトを考えてください\n"
                    "条件：\n"
                    "・画風は「明るくかわいらしい絵本風」\n"
                    "・主人公がどういう姿かも補足してください\n"
                    "・プロンプトは英語で書いてください\n"
                    "・ファンタジーすぎず、子供が見て安心できるイメージにしてください\n"
                    "・アートスタイルは「storybook illustration」\n"
                    "・髪色、目の色、服、年齢のプロンプトは必ず最初の方に記載してください\n"
                    "・以下のような形式を参考にしてください：\n"
                    "出力形式（例）：\n"
                    "a young girl with blonde hair wearing a blue dress, smiling in a flower garden, soft pastel colors, storybook illustration, children's picture book style, wide view, gentle lighting"
                    "プロンプトをこの形式だけで返してください。\n"
                    f"【ストーリー】：\n{story['結']}\n"
                )
            }
        ]
    )
    # 画像生成に受け渡すためのプロンプトをimage_prompt_2に格納
    #ストリームリット実装時はst.set_state(～～～)に格納する
    image_prompt = response.output_text
    image_prompts.append(image_prompt)  # image_prompt_4をリストに追加
    return image_prompts
    #これをsession_stateに格納して保存されるようにする



"""
画像生成を行う関数
ここで重要なのはimage_promptsから必要なプロンプトを抜き出すこと
now_pageはページ数を指定する変数→output(x)_scrapのコードに記載が必要
"""

def generate_image(image_prompts: list, now_page: int):
    stability_api_key = os.getenv("STABILITY_API_KEY")
    # image_promptは、上のコードからinputされたものを使えるように変更する。
    base_prompt = "masterpiece, best quality, ultra detailed, watercolor style, soft pastel palette, storybook illustration, children's picture book style, gentle lighting,"
    image_prompt = image_prompts[now_page]  # 1ページ目のプロンプトを取得

    response = requests.post(
        f"https://api.stability.ai/v2beta/stable-image/generate/sd3",
        headers={
            "authorization": f"Bearer {stability_api_key}",
            "accept": "image/*"
        },
        files={"none": ''},
        data={
            "model": "sd3.5-large-turbo", # sd3.5-large, sd3.5-large-turbo, sd3.5-medium から選ぶ
            "output_format": "jpeg",
            "prompt": base_prompt + image_prompt,
            "negative_prompt": "realistic photo, cluttered, grotesque, deformed hands, extra limbs, text, watermark",
            "style_preset": "origami",#とりあえず一旦origami固定でやってみる
        },
    )

    if response.status_code == 200:
        # 出力ファイルのパスを作成（例：./output/1.jpeg）
        output_path = f"./output/{now_page}.jpeg"
        # 出力フォルダ（./output）が存在しない場合は作成
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        # 取得した画像データをバイナリ形式でファイルに保存
        with open(output_path, 'wb') as file:
            file.write(response.content)
        # 保存した画像のファイルパスを返す（後で表示や処理に使える！）
        return output_path
    else:
        # エラーが返ってきた場合は例外を発生させて詳細を表示（API側のエラー内容が見れる！）
        raise Exception(str(response.json()))



"""
音声合成を行う関数
実際は下記の変数が必要
id = 'd158278c-c4fa-461a-b271-468146ad51c9'
text = 'ここにstory[起承転結]'
page = 1
voice_generated(id, text, page)
"""
#にじボイスAPIで合成した音声を生成
def voice_generated(id, text, page):
    url = f"https://api.nijivoice.com/api/platform/v1/voice-actors/{id}/generate-voice"

    payload = {
        "format": "mp3",
        "script": text,
        "speed": "1",
        "emotionalLevel": "0.1",
        "soundDuration": "0.1"
    }
    headers = {
        "accept": "application/json",
        "x-api-key": os.getenv("x_api_key"),
        "content-type": "application/json"
    }
    # にじボイスAPIにリクエスト送信
    response = requests.post(url, json=payload, headers=headers)
    result = response.json()
    #resultのaudioFileDownloadUrlにある音声データを取得
    download_url = result['generatedVoice']['audioFileDownloadUrl']
    response = requests.get(download_url)

    #指定先(今回はoutputフォルダ)に音声データを保存voice0.mp3みたいな感じ
    save_path = f'./output/voice{page}.mp3'
    if response.status_code == 200:
        with open(save_path, 'wb') as file:
            file.write(response.content)

st.write('apiは正常です')