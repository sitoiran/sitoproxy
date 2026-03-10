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
    """تست اتصال با سقف ۵ ثانیه برای پایداری بیشتر"""
    try:
        start_time = datetime.now()
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(5.0) # سقف ۵ ثانیه طبق درخواست شما
        result = sock.connect_ex((ip, int(port)))
        end_time = datetime.now()
        sock.close()
        if result == 0:
            return (end_time - start_time).total_seconds() * 1000
        return None
    except:
        return None

def get_best_mtproto():
    """استخراج پروکسی‌های MTProto با فیلتر پینگ زیر ۵۰۰۰"""
    sources = [
        "https://raw.githubusercontent.com/yebekhe/TelegramVipProxy/main/proxies.txt",
        "https://raw.githubusercontent.com/ZeiS-S/Telegram-Proxies/master/proxies.txt",
        "https://raw.githubusercontent.com/Bfanyzous/MTProto/main/mtproto.txt",
        "https://raw.githubusercontent.com/Sahab-S/Proxy-Collector/main/proxy.txt"
    ]
    
    links = []
    for url in sources:
        try:
            response = requests.get(url, timeout=20)
            if response.status_code == 200:
                # پیدا کردن تمام لینک‌های MTProto
                found = re.findall(r'tg://proxy\?[^\s"\'<>]+', response.text)
                links.extend(found)
        except: continue

    if not links: return None

    # انتخاب ۲۰ مورد برای تست پینگ
    sample = random.sample(links, min(len(links), 20))
    best_link = None
    min_ping = 5001 # شروع از بالای ۵۰۰۰

    for link in sample:
        try:
            server = re.search(r'server=([^&]+)', link).group(1)
            port = re.search(r'port=(\d+)', link).group(1)
            
            ping = check_proxy_ping(server, port)
            if ping and ping < 5000: # تایید پینگ‌های زیر ۵۰۰۰
                if ping < min_ping:
                    min_ping = ping
                    best_link = link
        except: continue
            
    # اگر هیچکدام زیر ۵۰۰۰ نبودند، یک مورد تصادفی برای خالی نماندن کانال بفرست
    return best_link if best_link else random.choice(links[:10])

def send_proxies():
    tehran_time = datetime.utcnow() + timedelta(hours=3, minutes=30)
    hour = tehran_time.hour
    
    if 6 <= hour < 12:
        greeting = "☀️ صبح بخیر! روزت رو با یک پروکسی پرسرعت شروع کن"
    elif 12 <= hour < 18:
        greeting = "☕️ وقت استراحته! با پروکسی‌های سی‌تو بدون وقفه در تلگرام باش"
    elif 18 <= hour < 24:
        greeting = "🌙 شب‌نشینی با سرعت بالا! بهترین پروکسی برای تماشای ویدیو"
    else:
        greeting = "🦉 شب‌گرد تنها؟ نگران قطعی نباش، سی‌تو بیداره"

    random_emoji = random.choice(["🚀", "💎", "⚡️", "🔥", "🌟", "🔋"])
    counter = hour + 1 

    proxy_link = get_best_mtproto()
    
    if proxy_link:
        text = (
            f"{random_emoji} **{greeting}**\n\n"
            f"✅ این {counter}اُمین پروکسی رایگان امروز است!\n"
            f"🚀 **پروکسی هوشمند MTProto با تست اتصال ارسال شد.**\n\n"
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
        print(f"✅ خروجی تلگرام: {r.status_code}")
    else:
        print("❌ متاسفانه هیچ پروکسی یافت نشد.")

if __name__ == "__main__":
    send_proxies()
