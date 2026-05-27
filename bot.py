import requests
import os
import json
import re

token = os.getenv('BOT_TOKEN')
chat_id = os.getenv('CHAT_ID')

# منابع تخصصی، معتبر و فعال پروکسی‌های تلگرام
sources = [
    "https://raw.githubusercontent.com/sk664/Telegram-Proxy/main/Socks5.txt",
    "https://raw.githubusercontent.com/ProxyCollector/Proxy/master/socks5.txt",
    "https://raw.githubusercontent.com/Zaeem20/Telegram-Proxy-Collector/main/Socks5.txt"
]

def fetch_valid_proxy():
    for url in sources:
        try:
            print(f"Trying source: {url}")
            response = requests.get(url, timeout=15)
            if response.status_code == 200 and response.text.strip():
                # پیدا کردن لینک‌های استاندارد پروکسی با استفاده از Regex
                proxies = re.findall(r'(tg://socks\?server=[^\s]+|https://t\.me/proxy\?server=[^\s]+)', response.text)
                if proxies:
                    # انتخاب یکی از پروکسی‌های تازه و فعال لیست
                    print("Successfully fetched an active proxy!")
                    return proxies[0].strip()
        except Exception as e:
            print(f"Failed to fetch from {url}: {e}")
            continue
    return None

def send_proxies():
    print("Process Started...")
    proxy_link = fetch_valid_proxy()
    
    if not proxy_link:
        print("❌ No active proxies found in any of the sources.")
        return

    try:
        # استانداردسازی لینک برای دکمه‌ها
        if proxy_link.startswith("tg://"):
            proxy_link = proxy_link.replace("tg://socks?", "https://t.me/proxy?")

        # متن لینک‌دار اختصاصی شما
        link_text = f"[⚡️ اتصال به پروکسی رایگان سی تو ⚡️]({proxy_link})"
        
        # ساخت دکمه شیشه‌ای زیر پیام
        reply_markup = {
            "inline_keyboard": [
                [
                    {"text": "💎 اتصال به پروکسی 💎", "url": proxy_link}
                ]
            ]
        }
        
        # چیدمان دقیق متن دلخواه شما
        text = (
            f"🌍 **پروکسی بین‌المللی سی‌تو (سرور خارج)**\n\n"
            f"{link_text}\n"
            f"{link_text}\n"
            f"{link_text}\n\n"
            f"❤️🤍💚\n"
            f"🆔 {chat_id}\n"
            f"🆔 {chat_id}\n"
            f"««««««««««««««««««««««\n\n"
            f"📢 کانال ما رو به دوستان خود معرفی کنید.\n"
            f"⏰ هر ۳۰ دقیقه یک پروکسی جدید و رایگان ارسال می شود.\n\n"
            f"🛍 جهت تهیه فیلترشکن اختصاصی (V2ray)، پر سرعت، بدون قطعی و در حال حاضر وصل از طریق ربات فیلترشکن سی تو ثبت سفارش کنید تا سریع تر کانفینگ و لینک ساب خود را دریافت کنید:\n"
            f"🤖 @vpnsitobot"
        )
        
        payload = {
            'chat_id': chat_id,
            'text': text,
            'parse_mode': 'Markdown',
            'reply_markup': json.dumps(reply_markup)
        }
        
        api_url = f"https://api.telegram.org/bot{token}/sendMessage"
        res = requests.post(api_url, data=payload)
        print(f"Telegram API Status: {res.status_code}")
        
    except Exception as e:
        print(f"Error in sending message: {e}")

if __name__ == "__main__":
    send_proxies()
