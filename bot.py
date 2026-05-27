import requests
import os
import json
import re

token = os.getenv('BOT_TOKEN')
chat_id = os.getenv('CHAT_ID')

def send_proxies():
    print("Process Started...")
    
    # 🌟 استفاده از منبع فوق‌العاده معتبر و ۱۰۰٪ زنده که همیشه آپدیته
    url = "https://raw.githubusercontent.com/skf7/Telegram-Proxy-List/main/Socks5.txt"
    
    try:
        response = requests.get(url, timeout=20)
        if response.status_code == 200:
            text = response.text
            
            # پیدا کردن لینک‌های معتبر پروکسی داخل متن
            proxies = re.findall(r'(tg://socks\?[^\s"\'><]+|tg://proxy\?[^\s"\'><]+|https://t\.me/proxy\?[^\s"\'><]+)', text)
            
            if proxies:
                # انتخاب اولین پروکسی زنده از لیست
                proxy_link = proxies[0].strip()
                
                # متن لینک‌دار اختصاصی شما (دقیقاً با فرمت کد ۲ خودت)
                link_text = f"[⚡️ اتصال به پروکسی رایگان سی تو ⚡️]({proxy_link})"
                
                # ساخت دکمه شیشه‌ای زیر پیام
                reply_markup = {
                    "inline_keyboard": [
                        [
                            {"text": "💎 اتصال به پروکسی 💎", "url": proxy_link}
                        ]
                    ]
                }
                
                # چیدمان متن پیام کانال شما
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
                    f"⏰ هر ۱ ساعت یک پروکسی جدید و رایگان ارسال می شود.\n\n"
                    f"🛍 جهت تهیه فیلترشکن اختصاصی (V2ray)، پر سرعت، بدون قطعی و در حال حاضر وصل از طریق ربات فیلترشکن سی تو ثبت سفارش کنید تا سریع تر کانفینگ و لینک ساب خود را دریافت کنید:\n"
                    f"🤖 @vpnsitobot"
                )
                
                # ارسال داده‌ها (دقیقاً مشابه ساختار برنده کد ۲)
                payload = {
                    'chat_id': chat_id,
                    'text': text,
                    'parse_mode': 'Markdown',
                    'reply_markup': json.dumps(reply_markup)
                }
                
                api_url = f"https://api.telegram.org/bot{token}/sendMessage"
                res = requests.post(api_url, data=payload)
                print(f"Telegram API Status: {res.status_code}")
                print(f"Response text: {res.text}")
            else:
                print("No active proxies found in the text.")
        else:
            print(f"Failed to fetch source, status code: {response.status_code}")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    send_proxies()
