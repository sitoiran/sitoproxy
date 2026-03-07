import requests
import os

token = os.getenv('BOT_TOKEN')
chat_id = os.getenv('CHAT_ID')

# منبع جدید، معتبر و تست شده
source_url = "https://raw.githubusercontent.com/IranianCypherpunks/MTProto-Proxies/main/mtproto_proxies.txt"

def send_proxies():
    print(f"Connecting to source...")
    try:
        response = requests.get(source_url, timeout=20)
        if response.status_code == 200:
            # پیدا کردن لینک‌های پروکسی که با tg://proxy شروع می‌شوند
            lines = response.text.split('\n')
            proxies = [l.strip() for l in lines if 'tg://proxy?server=' in l or 't.me/proxy?proxy=' in l]
            
            if not proxies:
                print("No proxies found in the text. Trying alternative format...")
                # برخی منابع لینک‌ها رو مستقیم می‌ذارن
                proxies = [l.strip() for l in lines if 'proxy' in l.lower() and 'http' not in l.lower()]

            print(f"Found {len(proxies)} potential proxies. Sending top 3...")
            
            count = 0
            for proxy_link in proxies[:3]:
                # اصلاح لینک برای نمایش بهتر در تلگرام
                formatted_link = proxy_link.replace('tg://', 'https://t.me/')
                
                text = f"🚀 **پروکسی جدید سی‌تو**\n\n🔗 {formatted_link}\n\n🆔 {chat_id}"
                url = f"https://api.telegram.org/bot{token}/sendMessage"
                res = requests.post(url, data={'chat_id': chat_id, 'text': text, 'parse_mode': 'Markdown'})
                print(f"Proxy {count+1} Status: {res.status_code}")
                count += 1
                
            if count == 0:
                print("Could not extract any valid proxy links.")
        else:
            print(f"Source Error: {response.status_code}")
    except Exception as e:
        print(f"System Error: {e}")

if __name__ == "__main__":
    send_proxies()
