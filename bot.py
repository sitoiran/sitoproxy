import requests
import os
import re
import json
import random
from datetime import datetime, timedelta

token = os.getenv('BOT_TOKEN')
chat_id = os.getenv('CHAT_ID')

def get_best_proxies():
    # استفاده از منابعی که پروکسی‌های MTProto تازه دارند
    sources = [
        "https://raw.githubusercontent.com/yebekhe/TelegramVipProxy/main/proxies.txt",
        "https://raw.githubusercontent.com/ZeiS-S/Telegram-Proxies/master/proxies.txt",
        "https://raw.githubusercontent.com/Sahab-S/Proxy-Collector/main/proxy.txt",
        "https://raw.githubusercontent.com/Bfanyzous/MTProto/main/mtproto.txt"
    ]
    for url in sources:
        try:
            response = requests.get(url, timeout=15)
            if response.status_code == 200:
                # پیدا کردن لینک‌های MTProto (شروع با tg://proxy)
                proxies = re.findall(r'tg://proxy\?[^\s"\'<>]+', response.text)
                if proxies: 
                    # انتخاب یکی از ۱۰ تای آخر (چون معمولاً تازه‌تر هستند)
                    return random.choice(proxies[-10:])
        except: continue
    return None

def send_proxies():
    # تنظیم ساعت به وقت ایران (UTC + 3:30)
    tehran_time = datetime.utcnow() + timedelta(hours=3, minutes=30)
    hour = tehran_time.hour
    
    # انتخاب متن بر اساس بازه زمانی ایران
    if 6 <= hour < 12:
        greeting = "☀️ صبح بخیر! روزت رو با یک پروکسی پرسرعت شروع کن"
    elif 12 <= hour < 18:
        greeting = "☕️ وقت استراحته! با پروکسی‌های سی‌تو بدون وقفه داخل تلگرام کانال‌گردی کن"
    elif 18 <= hour < 24:
        greeting = "🌙 شب‌نشینی با سرعت بالا! بهترین پروکسی برای تماشای ویدیو و چت در تلگرام"
    else:
        greeting = "🦉 شب‌گرد تنها؟ نگران قطعی نباش، سی‌تو بیداره"

    # انتخاب ایموجی تصادفی
    emojis = ["🚀", "💎", "⚡️", "🔥", "🌟", "🔋", "🛸", "🛰"]
    random_emoji = random.choice(emojis)
    
    counter = hour + 1 

    proxy_link = get_best_proxies()
    if proxy_link:
        text = (
            f"{random_emoji} **{greeting}**\n\n"
            f"✅ این {counter}اُمین پروکسی رایگان امروز است!\n"
            f"🚀 سرور با سرعت عالی آماده اتصال مستقیم است.\n\n"
            f"❤️🤍💚\n"
            f"🆔 {chat_id}\n"
            f"««««««««««««««««««««««\n\n"
            f"📢 کانال ما را به دوستان خود معرفی کنید.\n"
            f"⏰ **هر ساعت یک پروکسی جدید و رایگان ارسال می‌شود.**\n\n"
            f"🛍 جهت تهیه فیلترشکن اختصاصی (V2ray)، پر سرعت و بدون قطعی، کلمه **«سی تو»** را به آیدی زیر ارسال 👇 نمایید:\n"
            f"👤 @vpnsito"
        )
        
        reply_markup = {"inline_keyboard": [[{"text": f"{random_emoji} اتصال مستقیم به پروکسی {random_emoji}", "url": proxy_link}]]}
        
        api_url = f"https://api.telegram.org/bot{token}/sendMessage"
        payload = {
            'chat_id': chat_id,
            'text': text,
            'parse_mode': 'Markdown',
            'reply_markup': json.dumps(reply_markup),
            'disable_web_page_preview': True
        }
        
        res = requests.post(api_url, data=payload)
        print(f"✅ ارسال موفق در ساعت {hour} ایران")
    else:
        print("❌ پروکسی پیدا نشد.")

if __name__ == "__main__":
    send_proxies()
