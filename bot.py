import requests
import os

token = os.getenv('BOT_TOKEN')
chat_id = os.getenv('CHAT_ID')

# منبع جدید و تست شده (لینک مستقیم پروکسی‌های MTProto)
source_url = "https://raw.githubusercontent.com/Vannilla-Ice/MTProto-Collect/main/MTProto.txt"

def send_proxies():
    print(f"Target Chat: {chat_id}")
    try:
        response = requests.get(source_url, timeout=15)
        if response.status_code == 200:
            # جدا کردن خطوط و فیلتر کردن لینک‌های پروکسی
            lines = response.text.split('\n')
            proxies = [l.strip() for l in lines if 't.me/proxy?proxy=' in l]
            
            print(f"Found {len(proxies)} proxies. Sending top 3...")
            
            count = 0
            for proxy_link in proxies[:3]: # فقط 3 تای اول
                text = f"🚀 **پروکسی جدید سی‌تو**\n\n🔗 {proxy_link}\n\n🆔 {chat_id}"
                url = f"https://api.telegram.org/bot{token}/sendMessage"
                res = requests.post(url, data={'chat_id': chat_id, 'text': text, 'parse_mode': 'Markdown'})
                print(f"Proxy {count+1} Result: {res.text}")
                count += 1
                
            if count == 0:
                print("No valid proxy links found in the text.")
        else:
            print(f"Error: Source returned status code {response.status_code}")
    except Exception as e:
        print(f"Critical Error: {e}")

if __name__ == "__main__":
    send_proxies()
