import requests
import os
import re
import json
import random
from datetime import datetime, timedelta

token = os.getenv('BOT_TOKEN')
chat_id = os.getenv('CHAT_ID')

def get_best_mtproto():
    """دریافت پروکسی‌های MTProto از منابع معتبر و تازه"""
    sources = [
        "https://raw.githubusercontent.com/yebekhe/TelegramVipProxy/main/proxies.txt",
        "https://raw.githubusercontent.com/ZeiS-S/Telegram-Proxies/master/proxies.txt",
        "https://raw.githubusercontent.com/Bfanyzous/MTProto/main/mtproto.txt",
        "https://raw.githubusercontent.com/Midneight/tg-proxies/master/proxies.txt"
    ]
    
    links = []
    for url in sources:
        try:
            response = requests.get(url, timeout=15)
            if response.status_code == 200:
                # استخراج لینک‌های MTProto
                found = re.findall(r'tg://proxy\?server=[^&\s]+&port=\d+&secret=[^&\s]+', response.text)
                links.extend(found)
        except: continue

    if links:
        # به جای تست پینگ پیچیده، از بین ۵۰تای اول که تازه‌ترین‌ها هستند، یکی را تصادفی انتخاب می‌کنیم
        # این کار شانس سالم بودن در ایران را بالاتر می‌برد
        return random.choice(links[:50])
    return None

def send_proxies():
    tehran_time = datetime.utcnow() + timedelta(hours=3, minutes=30)
    hour = tehran_time.hour
    
    if 6 <= hour < 12:
        greeting = "☀️ صبح بخیر! روزت رو با یک پروکسی پرسرعت شروع کن"
    elif 12 <= hour < 18:
        greeting = "☕️ وقت استراحته! با پروکسی‌های سی‌تو بدون وقفه داخل تلگرام کانال‌گردی کن"
    elif 18 <= hour < 24:
        greeting = "🌙 شب‌نشینی با سرعت بالا! بهترین پروکسی برای تماشای ویدیو و چت در تلگرام"
    else:
        greeting = "🦉 شب‌گرد تنها؟ نگران قطعی نباش، سی‌تو بیداره"

    random_emoji = random.choice(["🚀", "💎", "⚡️", "🔥", "🌟", "🔋"])
    counter = hour + 1 

    proxy_link = get_best_mtproto()
    
    if proxy_link:
        text = (
            f"{random_emoji} **{greeting}**\n\n"
            f"✅ این {counter}اُمین پروکسی رایگان امروز است!\n"
            f"🚀 **پروکسی هوشمند MTProto آماده اتصال است.**\n\n"
            f"❤️🤍💚\n"
            f"🆔 {chat_id}\n"
            f"««««««««««««««««««««««\n\n"
            f"📢 کانال ما را به دوستان خود معرفی کنید.\n"
            f"⏰ **هر ساعت یک پروکسی جدید و رایگان ارسال می‌شود.**\n\n"
            f"🛍 جهت تهیه فیلترشکن اختصاصی (V2ray)، کلمه **«سی تو»** را به آیدی زیر ارسال 👇 نمایید:\n"
            f"👤 @vpnsito"
        )
        
        reply_markup = {"inline_keyboard": [[{"text": f"{random_emoji} اتصال به پروکسی {random_emoji}", "url": proxy_link}]]}
        
        payload = {
            'chat_id': chat_id,
            'text': text,
            'parse_mode': 'Markdown',
            'reply_markup': json.dumps(reply_markup),
            'disable_web_page_preview': True
        }
        
        r = requests.post(f"https://api.telegram.org/bot{token}/sendMessage", data=payload)
        if r.status_code == 200:
            print("✅ ارسال با موفقیت انجام شد.")
        else:
            print(f"❌ خطا در ارسال به تلگرام: {r.text}")
    else:
        print("❌ هیچ پروکسی در منابع پیدا نشد.")

if __name__ == "__main__":
    send_proxies()
