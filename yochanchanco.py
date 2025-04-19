###　mainかpage_inofoにおく

from openai import OpenAI
import os
from dotenv import load_dotenv
load_dotenv()

import json

import requests # stability.ai用


### 受け取る！！！！！　その１（1/2）

sex_options = "男の子"
job_options = "魔法使い"
theme_options = "ファンタジー"
preset_options = "enhance"


###　絵本作るのボタンが押されたとき

def make_story_gpt(sex, job, theme): # gptで物語つくる
    openai_api_key = os.getenv("OPENAI_API_KEY")
    client = OpenAI(api_key=openai_api_key,)

    response = client.responses.create(
        model="gpt-4.1", # gpt-4.1, gpt-4.1-mini から選ぶ
        input=[
            {
                "role": "system",
                "content": "あなたはプロフェッショナルな3歳児向けの絵本作家です。"
            },
            {
                "role": "user",
                "content": (
                    "以下の【input条件】と【出力要件】に沿って、新しい物語を創作してください。json形式で出力してください\n"
                    "\n"
                    "【input条件】\n"
                    f"--主人公の性別：{sex}\n" # このあたりの条件はinputから変数で取得するように変更する
                    f"--主人公のジョブ：{job}\n"
                    f"--結末の雰囲気：{theme}\n"
                    "\n"
                    "【出力要件】\n"
                    "・登場人物は主人公と副主人公の2キャラクターのみとしてください。物語の途中で、追加のキャラクターを登場させていはいけません。\n"
                    "・人形（doll）や卵（egg）や像（statue）や鏡（mirror）は登場してはいけません。\n"
                    "・主人公と副主人公の名前に関して、「ミッキー」などの特定の物語をイメージさせるものは利用してはいけません。\n"
                    "・ネズミ（mouse）とふくろう（owl）の登場を禁止します。\n"
                    "・物語の出力は、【出力されるjson形式のサンプル】に倣って、起承転結および主人公像、副主人公像の6つに分けてください。各200字程度で、計1200字程度で記述してください。\n"
                    "・主人公と副主人公は、起承転結のそれぞれの物語に必ず登場するようにしてください。\n"
                    "・主人公と副主人公については、その外見的特徴（服装、ヘアスタイル、ヘアカラー、アイカラー、持ち物など）を含めて記述してください。\n"
                    "・主人公と副主人公に関する色の表現には、「光る」や「虹色の」など、描写が難しいものは避けてください。\n"
                    "\n"
                    "【出力されるjson形式のサンプル】\n"
                    "{\n"
                    "  '起': 'むかしむかし、お城の中に、ひまわり色のドレスを着たお姫さまのエミリーちゃんがくらしていました。エミリーちゃんは、ふんわり茶色のくるくる髪と、やさしいこげちゃ色の目をしています。となりにはいつも、青いリボンを巻いた、元気なうさぎのリリーちゃんがいます。リリーちゃんは、白くてふわふわの毛と、まん丸な黒い目がキラキラしています。ふたりはとても仲良しです。',\n"
                    "  '承': 'ある日、エミリーちゃんとリリーちゃんは、お城のにわで虫めがねを見つけました。『これで何か探してみよう！』とエミリーちゃんが言いました。リリーちゃんは『かくれんぼの宝物が見つかるかも！』とわくわく。ふたりは大きな木の下やお花畑をのぞいて歩きます。でも、見つかるのは葉っぱや小石ばかり。もっとふしぎな物をさがして、ふたりはお庭の奥へ進んでいきました。',\n"
                    "  '転': 'お庭のいちばん奥で、ふたりは小さな穴を見つけました。『虫めがねでのぞいてみよう！』とエミリーちゃん。リリーちゃんはドキドキしながらエミリーちゃんの肩にのぼります。虫めがねを通してのぞいたら、なんと奥に小さなキラキラした何かが見えます。『なにかな？』『お宝かも！』ふたりは思いきって小さな穴を広げようとしました。すると、その奥からふんわり風が吹いてきて…。',\n"
                    "  '結': 'ふたりが目をとじると、なんと穴の中からは美味しそうなにんじんケーキの香りがぷ～ん！『えっ！ケーキみつけたの！？』とびっくり。嬉しくなったエミリーちゃんとリリーちゃんは、ふたりだけの小さな秘密のお部屋に入り、しあわせいっぱいケーキを食べました。まさかお庭の奥でケーキが見つかるなんて、ほんとうにびっくりの一日でした！',\n"
                    "  '主人公': 'エミリーちゃんは、ひまわり色のドレスを着たやさしいお姫さまです。茶色のくるくるとした長い髪をしていて、こげちゃ色のはっきりした目が特徴。楽しいことや探検が大好きで、明るく前向きな女の子です。小さなことにもワクワクし、困っている友だちにはいつも手をさしのべます。',\n"
                    "  '副主人公': 'リリーちゃんは、青いリボンを首に巻いた、元気なうさぎです。まっ白でふわふわの毛と、まん丸な黒い目がチャームポイント。エミリーちゃんのよき相棒で、明るくて好奇心いっぱい。小さい体なのに、どんなときもエミリーちゃんの冒険にいっしょうけんめい付きあってくれる大事なともだちです。'\n"
                    "}"
                )
            }
        ]
    )

    story = json.loads(response.output_text)
    return story



gpted_story = make_story_gpt(sex_options, job_options, theme_options)


###　絵本作るのボタンが押されたとき

def make_image_prompt_gpt(story): # gptで画像生成プロンプトのパーツつくる
    openai_api_key = os.getenv("OPENAI_API_KEY")
    client = OpenAI(api_key=openai_api_key,)

    response = client.responses.create(
        model="gpt-4.1", # gpt-4.1, gpt-4.1-mini から選ぶ
        input=[
            {
                "role": "system",
                "content": "あなたはプロフェッショナルな画像生成AI（Stable Diffusion）のプロンプトエンジニアです。要件に沿って、画像生成プロンプトのパーツを作成してください。"
            },
            {
                "role": "user",
                "content": (
                    "以下の【story】をベースにして、英語で、画像生成プロンプトのパーツを作成してください。【画像生成プロンプトの注意事項】は必ず順守してください。json形式で出力してください\n"
                    "\n"
                    "【story】\n"
                    f"{story}\n"
                    "\n"
                    "【画像生成プロンプトの注意事項】\n"
                    "・Subject_Depiction_起、Subject_Depiction_承'、Subject_Depiction_転、Subject_Depiction_結については、それぞれ16words以内で考えてください。最初に、「scene:」を宣言してください。また、main_Characterとsub_Characterの名前を含め、main_Characterとsub_Characterの行動や状態を端的に記述してください。\n"
                    "・main_Character_Traits、sub_Character_Traitsについては、それぞれ17words以内で考えてください。最初に、主人公格（main-Protagonist: かsub-Protagonist: ）と名前を宣言してください。その後、人物像（動物像）を端的に表現し、続いて外見的特徴（服装、ヘアスタイル、ヘアカラー、アイカラー、小物など）を中心に記述してください。\n"
                    "・Artistic_Styleは、watercolor styleがおススメです。より適当なものがあれば、そちらを採用してください。\n"
                    "・Color_Paletteは、soft pastel toneがおススメです。より適当なものがあれば、そちらを採用してください。\n"
                    "・Background_起、Background_承、Background_転、Background_結については、それぞれ10words以内で考えてください。全体の世界観を維持しつつ、各物語に適した背景の状態や雰囲気を記述してください。\n"
                    "\n"
                    "【出力されるjson形式のサンプル】\n"
                    "{{\n"
                    "  'Artistic_Style': 'watercolor style',\n"
                    "  'Lighting': 'bright and gentle daylight,\n"
                    "  'Color_Palette': 'soft pastel tone',\n"
                    "  'Subject_Depiction_起': 'Princess Emily in sunflower dress with Lily, the blue-ribboned white rabbit',\n"
                    "  'Subject_Depiction_承': 'Emily and Lily excited, exploring castle garden with magnifying glass',\n"
                    "  'Subject_Depiction_転': 'Emily peers into tiny hole, Lily on shoulder, magical sparkles beyond',\n"
                    "  'Subject_Depiction_結': 'Emily and Lily joyful in hidden room, sharing carrot cake together',\n"
                    "  'main_Character_Traits': 'main-Protagonist: Leo – a small prince with short golden hair, vivid blue eyes, tidy royal attire and a flowing red cape',\n"
                    "  'sub_Character_Traits': 'sub-Protagonist: Tino – a cute little grey mouse with pink ears, a thick tail and a bright yellow scarf fluttering playfully',\n"
                    "  'Background_起': 'bright castle interior, sunlight through grand windows',\n"
                    "  'Background_承': 'lush castle garden with old trees, blooming flowers everywhere',\n"
                    "  'Background_転': 'shaded garden corner, mysterious tiny hole near old roots',\n"
                    "  'Background_結': 'cozy secret room, softly lit, table set with carrot cake',\n"
                    "  'Composition': 'storybook-inspired, clear character focus, gentle whimsical touch',\n"
                    "}}"
                )
            }
        ]
    )
    
    parts = json.loads(response.output_text)
    return parts



gpted_prompt_parts = make_image_prompt_gpt(gpted_story)


###　絵本作るのボタンが押されたとき
###　（プロンプト自体は起承転結分が全て作成されてしまうので、セッションに保存しておきたい）

def concat_image_prompt(parts): # パーツをつなげて起承転結の画像生成プロンプトをつくる

    Artistic_Style = parts["Artistic_Style"]
    Lighting = parts["Lighting"]
    Color_Palette = parts["Color_Palette"]
    Subject_Depiction_起 = parts["Subject_Depiction_起"]
    Subject_Depiction_承 = parts["Subject_Depiction_承"]
    Subject_Depiction_転 = parts["Subject_Depiction_転"]
    Subject_Depiction_結 = parts["Subject_Depiction_結"]
    main_Character_Traits = parts["main_Character_Traits"]
    sub_Character_Traits = parts["sub_Character_Traits"]
    Background_起 = parts["Background_起"]
    Background_承 = parts["Background_承"]
    Background_転 = parts["Background_転"]
    Background_結 = parts["Background_結"]
    Composition = parts["Composition"]

    common_image_prompt = f"masterpiece, best quality, anime screencap, chibi, {Artistic_Style}, {Lighting}, {Color_Palette}"

    image_prompt_起 = f"{common_image_prompt}, BREAK {Subject_Depiction_起}; {main_Character_Traits}; {sub_Character_Traits}; BREAK {Background_起}; {Composition}"
    image_prompt_承 = f"{common_image_prompt}, BREAK {Subject_Depiction_承}; {main_Character_Traits}; {sub_Character_Traits}; BREAK {Background_承}; {Composition}"
    image_prompt_転 = f"{common_image_prompt}, BREAK {Subject_Depiction_転}; {main_Character_Traits}; {sub_Character_Traits}; BREAK {Background_転}; {Composition}"
    image_prompt_結 = f"{common_image_prompt}, BREAK {Subject_Depiction_結}; {main_Character_Traits}; {sub_Character_Traits}; BREAK {Background_結}; {Composition}"

    image_prompt_all = [image_prompt_起, image_prompt_承, image_prompt_転, image_prompt_結]

    return image_prompt_all


merged_listed_prompts = concat_image_prompt(gpted_prompt_parts)

### 受け取る！！！！！　その２（2/2）　セッション情報にあるはずなので、頑張って受け取る
page = 0


###　ページに応じて違う画像を生成することができる　→　絵本作るのボタンで、1枚分作って、その後はどうするか悩む

def make_image_stability(image_prompt_all, preset, now_page): # Stability.aiで画像つくる（いったん1枚だけ）
    stability_api_key = os.getenv("STABILITY_API_KEY")
    
    image_prompt = image_prompt_all[now_page]

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
            "prompt": image_prompt,
            "negative_prompt": "realistic photo, cluttered, grotesque, anatomically incorrect, deformed hands, extra limbs, animal anthropomorphism, text, watermark",
            "style_preset": preset, # inputを受け取れるようにする
        },
    )


    if response.status_code != 200:
        raise RuntimeError(f"Stability API error: {response.status_code} – {response.text}")

    if response.status_code == 200:
        with open(f"./out/{now_page}.jpeg", 'wb') as file:
            file.write(response.content)
    else:
        raise Exception(str(response.json()))
    return f"./out/{now_page}.jpeg"




###　この画像の受け渡し方が分からん。とりあえず/outに入る

make_image_stability(merged_listed_prompts, preset_options, page)

