import requests
import os
from dotenv import load_dotenv

#環境変数の読み込み
load_dotenv()

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
        "x-api-key": os.getenv("x-api-key"),
        "content-type": "application/json"
    }
    response = requests.post(url, json=payload, headers=headers)
    result = response.json()

    response = requests.get(download_url)
    download_url = result['generatedVoice']['audioFileDownloadUrl']
    save_path = f'./output/voice{page}.mp3'
    if response.status_code == 200:
        with open(save_path, 'wb') as file:
            file.write(response.content)