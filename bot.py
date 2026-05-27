import requests
import os
import json
import re

token = os.getenv('BOT_TOKEN')
chat_id = os.getenv('CHAT_ID')

# منابع فوق‌العاده فعال و تست شده که همیشه پروکسی دارند
sources = [
    "https://raw.githubusercontent.com/yebekhe/TelegramV2rayCollector/main/sub/MTProto",
    "https://raw.githubusercontent.com/altanyvpn/telegram-proxy/main/list.txt",
    "https://raw.githubusercontent.com/Zaeem20/Telegram-Proxy-Collector/main/Socks5.txt"
]

def fetch_valid_proxy():
    for url in sources:
        try:
            print(f"Trying source: {url}")
            response = requests.get(url, timeout=15)
            if response.status_code == 200:
                text = response.text
                # یک جستجوی ساده و منعطف برای پیدا کردن هر نوع لینک پروکسی تلگرام
                proxies = re.findall(r'(t\.me/proxy\?server=[^\s"\'><]+|tg://socks\?[^\s"\'><]+|tg://proxy\?[^\s"\'><]+)', text)
                
                if proxies:
                    found_proxy = proxies[0].strip()
                    # استانداردسازی لینک برای تلگرام
                    if found_proxy.startswith("t.me"):
                        found_proxy = "https://" + found_proxy
                    elif found_proxy.startswith("tg://socks?"):
                        found_proxy = found_proxy.replace("tg://socks?", "https://t.me/proxy?")
                    elif found_proxy.startswith("tg://proxy?"):
                        found_proxy = found_proxy.replace("tg://proxy?", "https://t.me/proxy?")
                        
                    print(f"🎯 Found proxy: {found_proxy}")
                    return found_proxy
        except Exception as e:
            print(f"Error fetching from {url}: {e}")
            continue
    return None

def send_proxies():
    print("Process Started...")
    proxy_link = fetch_valid_proxy()
    
    if not proxy_link:
        print("❌ دیتایی از منابع دریافت نشد یا فرمت لینک‌ها تغییر کرده است.")
        return

    try:
        # متن لینک‌دار اختصاصی شما
        link_text = f"[⚡️ اتصال به پروکسی رایگان سی تو ⚡️]({proxy_link})"
        
        # دکمه شیشه‌ای زیر پیام
        reply_markup = {
            "inline_keyboard": [
                [
                    {"text": "💎 اتصال به پروکسی 💎", "url": proxy_link}
                ]
            ]
        }
        
        # چیدمان متن نهایی شما
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
        if res.status_code != 200:
            print(f"Telegram Response Error: {res.text}")
            
    except Exception as e:
        print(f"Error in sending message: {e}")

if __name__ == "__main__":
    send_proxies()
