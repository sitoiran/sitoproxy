import requests
import os
import re
import json
import random
import socket
from datetime import datetime, timedelta

token = os.getenv('BOT_TOKEN')
chat_id = os.getenv('CHAT_ID')

def check_proxy_ping(ip, port):
    """تست اتصال فیزیکی به سرور پروکسی"""
    try:
        start_time = datetime.now()
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(2.0)
        result = sock.connect_ex((ip, int(port)))
        end_time = datetime.now()
        sock.close()
        if result == 0:
            return (end_time - start_time).total_seconds() * 1000
        return None
    except:
        return None

def get_best_mtproto():
    """استخراج و گلچین بهترین پروکسی‌های MTProto"""
    sources = [
        "https://raw.githubusercontent.com/yebekhe/TelegramVipProxy/main/proxies.txt",
        "https://raw.githubusercontent.com/ZeiS-S/Telegram-Proxies/master/proxies.txt",
        "https://raw.githubusercontent.com/Bfanyzous/MTProto/main/mtproto.txt"
    ]
    
    links = []
    for url in sources:
        try:
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                # جستجو برای لینک‌های MTProto
                found = re.findall(r'tg://proxy\?server=[^&\s]+&port=\d+&secret=[^&\s]+', response.text)
                links.extend(found)
        except: continue

    if not links: return None

    # تست پینگ روی ۱۰ مورد تصادفی برای پیدا کردن سریع‌ترین
    sample = random.sample(links, min(len(links), 10))
    best_link = None
    min_ping = 9999

    for link in sample:
        # استخراج IP و Port از لینک برای تست پینگ
        server = re.search(r'server=([^&]+)', link).group(1)
        port = re.search(r'port=(\d+)', link).group(1)
        
        ping = check_proxy_ping(server, port)
        if ping and ping < min_ping:
            min_ping = ping
            best_link = link
            
    return best_link

def send_proxies():
    tehran_time = datetime.utcnow() + timedelta(hours=3, minutes=30)
    hour = tehran_time.hour
    
    # پیام‌های بازه زمانی (طبق تنظیمات قبلی شما)
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
            f"🚀 **پروکسی هوشمند MTProto با پینگ پایین انتخاب شد.**\n\n"
            f"❤️🤍💚\n"
            f"🆔 {chat_id}\n"
            f"««««««««««««««««««««««\n\n"
            f"📢 کانال ما را به دوستان خود معرفی کنید.\n"
            f"⏰ **هر ساعت یک پروکسی جدید و رایگان ارسال می‌شود.**\n\n"
            f"🛍 جهت تهیه فیلترشکن اختصاصی (V2ray)، کلمه **«سی تو»** را به آیدی زیر ارسال 👇 نمایید:\n"
            f"👤 @vpnsito"
        )
        
        reply_markup = {"inline_keyboard": [[{"text": f"{random_emoji} اتصال مستقیم به پروکسی {random_emoji}", "url": proxy_link}]]}
        
        payload = {
            'chat_id': chat_id,
            'text': text,
            'parse_mode': 'Markdown',
            'reply_markup': json.dumps(reply_markup),
            'disable_web_page_preview': True
        }
        
        requests.post(f"https://api.telegram.org/bot{token}/sendMessage", data=payload)
    else:
        print("❌ پروکسی MTProto سالمی پیدا نشد.")

if __name__ == "__main__":
    send_proxies()
