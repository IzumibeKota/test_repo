import sys
import json
import requests
from datetime import datetime # datetime モジュールをインポート

def send_teams_notification(webhook_url, message_text):
    headers = {
        'Content-Type': 'application/json; charset=utf-8' # ここに charset=utf-8 を追加
    }

    # 現在時刻をフォーマット
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # message_text からビルドURLを抽出（既存のロジックを保持）
    build_url = ""
    # "ビルド成功：[ビルドURL](http://...)" の形式を想定
    if '[' in message_text and ']' in message_text and '(' in message_text and ')' in message_text:
        try:
            # 括弧内のURLを抽出する正規表現または文字列操作
            # ここではシンプルな文字列操作で、最後の括弧の内容をURLとして抽出
            start_paren = message_text.rfind('(')
            end_paren = message_text.rfind(')')
            if start_paren != -1 and end_paren != -1 and start_paren < end_paren:
                build_url = message_text[start_paren + 1:end_paren]
        except Exception as e:
            print(f"Failed to extract build URL: {e}", file=sys.stderr)


    payload = {
        "@type": "MessageCard",
        "@context": "http://schema.org/extensions",
        "themeColor": "0076D7", # 青
        "summary": "Jenkins Build Notification",
        "sections": [
            {
                "activityTitle": "Jenkins ビルド通知",
                "activitySubtitle": message_text, # ここは Jenkinsfile から渡された生メッセージ
                "facts": [
                    {
                        "name": "プロジェクト",
                        "value": "Jenkins Pipeline"
                    },
                    {
                        "name": "時刻",
                        "value": current_time # ここに動的な時刻をセット
                    }
                ],
                "markdown": True
            }
        ],
        "potentialAction": [] # 初期化
    }

    # ビルドURLがある場合のみ potentialAction を追加
    if build_url:
        payload["potentialAction"].append({
            "@type": "OpenUri",
            "name": "ビルド結果を見る",
            "targets": [
                {
                    "os": "default",
                    "uri": build_url
                }
            ]
        })

    try:
        # json.dumps に ensure_ascii=False を追加
        response = requests.post(webhook_url, headers=headers, data=json.dumps(payload, ensure_ascii=False).encode('utf-8'))
        response.raise_for_status() # HTTPエラーがあれば例外を発生させる
        print(f"Teams notification sent successfully. Status: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"Failed to send Teams notification: {e}", file=sys.stderr)
        sys.exit(1) # エラー時にスクリプトを終了させる

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python send_message_build.py <webhook_url> <message_text>", file=sys.stderr)
        sys.exit(1)

    webhook_url = sys.argv[1]
    message_text = sys.argv[2]
    send_teams_notification(webhook_url, message_text)