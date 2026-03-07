import requests
import os

# خواندن اطلاعات از Secrets
token = os.getenv('BOT_TOKEN')
chat_id = os.getenv('CHAT_ID')

# منبع جایگزین (مطمئن‌تر)
source_url = "https://raw.githubusercontent.com/yebekhe/TelegramV2rayCollector/main/sub/MTProto"

def send_proxies():
    print(f"Target Chat: {chat_id}") # برای تست که ببینیم آیدی درسته یا نه
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
                    
                    # ارسال و چاپ نتیجه دقیق
                    res = requests.post(url, data={'chat_id': chat_id, 'text': text, 'parse_mode': 'Markdown'})
                    print(f"Try sending proxy {count+1}: {res.status_code} - {res.text}")
                    count += 1
            if count == 0:
                print("No proxy links found in the source URL!")
        else:
            print(f"Error fetching source: {response.status_code}")
    except Exception as e:
        print(f"Critical Error: {e}")

if __name__ == "__main__":
    send_proxies()
