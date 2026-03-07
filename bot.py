import requests
import os

token = os.getenv('BOT_TOKEN')
chat_id = os.getenv('CHAT_ID')

# منبع فوق‌العاده معتبر با لینک‌های مستقیم MTProto
source_url = "https://raw.githubusercontent.com/yebekhe/TelegramV2rayCollector/main/sub/MTProto"

def send_proxies():
    try:
        response = requests.get(source_url, timeout=20)
        if response.status_code == 200:
            lines = response.text.split('\n')
            # پیدا کردن لینک‌هایی که با t.me/proxy شروع می‌شن
            proxies = [l.strip() for l in lines if 't.me/proxy?proxy=' in l]
            
            if proxies:
                # طبق خواسته شما: ارسال ۱ عدد پروکسی در هر نوبت
                proxy_link = proxies[0]
                text = f"🚀 **پروکسی جدید و پرسرعت سی‌تو**\n\n🔗 {proxy_link}\n\n🆔 {chat_id}"
                url = f"https://api.telegram.org/bot{token}/sendMessage"
                requests.post(url, data={'chat_id': chat_id, 'text': text, 'parse_mode': 'Markdown'})
                print("One direct proxy sent successfully!")
            else:
                print("No direct link found.")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    send_proxies()
