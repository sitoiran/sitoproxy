import requests
import os

token = os.getenv('BOT_TOKEN')
chat_id = os.getenv('CHAT_ID')
source_url = "https://raw.githubusercontent.com/yebekhe/TelegramV2rayCollector/main/sub/MTProto"

def send_proxies():
    print(f"Connecting to bot with token... {token[:10]}***")
    try:
        response = requests.get(source_url)
        if response.status_code == 200:
            lines = response.text.split('\n')
            count = 0
            for line in lines:
                if 't.me/proxy?proxy=' in line and count < 3:
                    proxy_link = line.strip()
                    text = f"🚀 **پروکسی جدید سی‌تو**\n\n🔗 {proxy_link}\n\n🆔 {chat_id}"
                    url = f"https://api.telegram.org/bot{token}/sendMessage"
                    res = requests.post(url, data={'chat_id': chat_id, 'text': text, 'parse_mode': 'Markdown'})
                    print(f"Telegram Response: {res.text}")
                    count += 1
            print(f"Finished. Sent {count} proxies.")
    except Exception as e:
        print(f"Error occurred: {e}")

if __name__ == "__main__":
    send_proxies()
