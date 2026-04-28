# send_teams_notification.py
import sys
import json
import requests

def send_teams_notification(webhook_url, message_text):
    headers = {
        'Content-Type': 'application/json'
    }

    # シンプルな MessageCard フォーマット
    # 必要に応じて Adaptive Card に変更することも可能
    payload = {
        "@type": "MessageCard",
        "@context": "http://schema.org/extensions",
        "themeColor": "0076D7", # 青
        "summary": "Jenkins Build Notification",
        "sections": [
            {
                "activityTitle": "Jenkins ビルド通知",
                "activitySubtitle": message_text,
                "facts": [
                    {
                        "name": "プロジェクト",
                        "value": "Jenkins Pipeline" # 必要に応じて動的に変更
                    },
                    {
                        "name": "時刻",
                        "value": "現在時刻" # Pythonで生成可能
                    }
                ],
                "markdown": True
            }
        ],
        "potentialAction": [
            {
                "@type": "OpenUri",
                "name": "ビルド結果を見る",
                "targets": [
                    {
                        "os": "default",
                        "uri": message_text.split('(')[1][:-1] if '[' in message_text and ']' in message_text else ""
                    }
                ]
            }
        ]
    }

    try:
        response = requests.post(webhook_url, headers=headers, data=json.dumps(payload))
        response.raise_for_status() # HTTPエラーがあれば例外を発生させる
        print(f"Teams notification sent successfully. Status: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"Failed to send Teams notification: {e}", file=sys.stderr)
        sys.exit(1) # エラー時にスクリプトを終了させる

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python send_teams_notification.py <webhook_url> <message_text>", file=sys.stderr)
        sys.exit(1)

    webhook_url = sys.argv[1]
    message_text = sys.argv[2]
    send_teams_notification(webhook_url, message_text)
