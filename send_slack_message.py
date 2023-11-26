import requests
import json
from jobcan_access import base_dir

def send_message(message):
    # credentials.json ファイルから Slack トークンや関連の情報を読み込む
    with open(base_dir() / 'credentials.json') as f:
        data = json.load(f)
    SLACK_USER_TOKEN = data["SLACK_USER_TOKEN"]
    SLACK_TEST_CHANNEL_ID = data["YOUR_SLACK_TEST_CHANNEL_ID"]
    SLACK_TIMECLOCK_CHANNEL_ID = data["SLACK_TIMECLOCK_CHANNEL_ID"]
    SLACK_API_URL = data["SLACK_API_URL"]

    # HTTP ヘッダーを設定
    headers = {
        "Authorization": f"Bearer {SLACK_USER_TOKEN}",
        "Content-Type": "application/json"
    }

    # メッセージによって Slack チャンネルを選択
    if message == "打刻表を確認します":
        payload = {
            "channel": SLACK_TEST_CHANNEL_ID,
            "text": message
        }
    else:
        payload = {
            "channel": SLACK_TIMECLOCK_CHANNEL_ID,
            "text": message
        }

    # Slack API にメッセージを投稿
    response = requests.post(SLACK_API_URL, headers=headers, json=payload)

    # レスポンスのステータスコードに基づいて成功または失敗を表示
    if response.status_code == 200:
        print("Slack上の送信が完了しました。")
    else:
        print(f"Slack上の送信が失敗しました。Status code: {response.status_code}, Response: {response.text}")
