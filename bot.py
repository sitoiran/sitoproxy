import requests
import os

token = os.getenv('BOT_TOKEN')
chat_id = os.getenv('CHAT_ID')

# منبع جدید و تست شده با لینک‌های مستقیم
source_url = "https://raw.githubusercontent.com/coldwater-10/MTProto_Proxy/main/mtproto.txt"

def send_proxies():
    try:
        response = requests.get(source_url, timeout=20)
        if response.status_code == 200:
            lines = response.text.split('\n')
            # استخراج لینک‌هایی که فرمت درست تلگرام دارند
            proxies = [l.strip() for l in lines if 't.me/proxy?proxy=' in l]
            
            if proxies:
                # فقط ارسال ۱ عدد پروکسی در هر بار اجرا طبق خواسته شما
                proxy_link = proxies[0]
                text = f"🚀 **پروکسی جدید و اختصاصی سی‌تو**\n\n🔗 {proxy_link}\n\n🆔 {chat_id}"
                url = f"https://api.telegram.org/bot{token}/sendMessage"
                requests.post(url, data={'chat_id': chat_id, 'text': text, 'parse_mode': 'Markdown'})
                print("Successfully sent 1 proxy.")
            else:
                print("No valid proxy links found.")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    send_proxies()
