import requests
import os

token = os.getenv('BOT_TOKEN')
chat_id = os.getenv('CHAT_ID')

def send_proxies():
    print("Process Started...")
    # منبع جایگزین و بسیار پایدار
    url = "https://raw.githubusercontent.com/yebekhe/TelegramV2rayCollector/main/sub/MTProto"
    
    try:
        print(f"Connecting to: {url}")
        response = requests.get(url, timeout=20)
        
        if response.status_code == 200:
            lines = response.text.split('\n')
            proxies = [l.strip() for l in lines if 't.me/proxy?proxy=' in l]
            
            if proxies:
                proxy = proxies[0]
                msg = f"🚀 **پروکسی جدید سی‌تو**\n\n🔗 {proxy}"
                api_url = f"https://api.telegram.org/bot{token}/sendMessage"
                res = requests.post(api_url, data={'chat_id': chat_id, 'text': msg, 'parse_mode': 'Markdown'})
                print(f"Telegram Response: {res.status_code}")
            else:
                print("No proxy found in file.")
        else:
            print(f"Source Error: {response.status_code}")
            
    except Exception as e:
        print(f"Error: {e}")

# این دو خط پایین خیلی مهم هستن، حتما باشن:
if __name__ == "__main__":
    send_proxies()
