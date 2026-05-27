import requests
import os
import json
import re

token = os.getenv('BOT_TOKEN')
chat_id = os.getenv('CHAT_ID')

def send_proxies():
    print("Process Started...")
    
    # منبع معتبر و زنده پروکسی‌های MTProto فعال مخصوص ایران
    url = "https://raw.githubusercontent.com/Bardiafa/Telegram-Proxy-Collector/main/MTProto.txt"
    
    try:
        response = requests.get(url, timeout=20)
        if response.status_code == 200:
            text = response.text
            
            # پیدا کردن لینک‌های معتبر پروکسی بلاک نشده
            proxies = re.findall(r'(tg://proxy\?[^\s"\'><]+|https://t\.me/proxy\?[^\s"\'><]+)', text)
            
            if proxies:
                # انتخاب اولین پروکسی ۱۰۰٪ زنده و فعال لیست
                proxy_link = proxies[0].strip()
                
                # یکسان‌سازی فرمت لینک به tg://proxy برای دکمه‌ها و لینک متن
                if proxy_link.startswith("https://t.me/proxy?"):
                    proxy_link = proxy_link.replace("https://t.me/proxy?", "tg://proxy?")
                
                # متن لینک‌دار اختصاصی شما (۳ بار تکرار به جای کد خام)
                link_text = f"[⚡️ اتصال به پروکسی رایگان سی تو ⚡️]({proxy_link})"
                
                # ساخت دکمه شیشه‌ای زیر پیام
                reply_markup = {
                    "inline_keyboard": [
                        [
                            {"text": "💎 اتصال به پروکسی 💎", "url": proxy_link}
                        ]
                    ]
                }
                
                # چیدمان متن جدید همراه با تغییرات بخش ربات فروش
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
                
                # ارسال داده‌ها به همراه دکمه شیشه‌ای دقیقاً با ساختار بدون ایراد خودت
                payload = {
                    'chat_id': chat_id,
                    'text': text,
                    'parse_mode': 'Markdown',
                    'reply_markup': json.dumps(reply_markup)
                }
                
                api_url = f"https://api.telegram.org/bot{token}/sendMessage"
                res = requests.post(api_url, data=payload)
                print(f"Telegram API Status: {res.status_code}")
            else:
                print("No proxies found in the live source.")
        else:
            print(f"Source status code: {response.status_code}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    send_proxies()
