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
    """تست واقعی پینگ برای اطمینان از سالم بودن پروکسی قبل از ارسال"""
    try:
        start_time = datetime.now()
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(3) # حداکثر ۳ ثانیه برای پاسخ
        result = sock.connect_ex((ip, int(port)))
        end_time = datetime.now()
        sock.close()
        if result == 0:
            return (end_time - start_time).total_seconds() * 1000
        return None
    except:
        return None

def get_best_proxies():
    # استفاده از منابعی که پروکسی‌های مشابه iRoProxy را منتشر می‌کنند
    sources = [
        "https://raw.githubusercontent.com/vfarid/proxy-list/main/socks5.txt",
        "https://raw.githubusercontent.com/Iranian-Hacker/Telegram-Proxies/master/proxies.txt",
        "https://raw.githubusercontent.com/mahdibland/ShadowsocksAggregator/master/sub/sub_merge.txt"
    ]
    
    all_found = []
    for url in sources:
        try:
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                all_found.extend(re.findall(r'\d+\.\d+\.\d+\.\d+:\d+', response.text))
        except: continue

    if not all_found: return None

    # انتخاب ۲۰ پروکسی تصادفی برای تست پینگ (برای صرفه‌جویی در زمان)
    sample_proxies = random.sample(all_found, min(len(all_found), 20))
    
    tested_proxies = []
    for p in sample_proxies:
        ip, port = p.split(':')
        ping = check_proxy_ping(ip, port)
        if ping:
            tested_proxies.append((p, ping))
    
    # مرتب‌سازی بر اساس کمترین پینگ
    if tested_proxies:
        tested_proxies.sort(key=lambda x: x[1])
        return tested_proxies[0][0] # بهترین پروکسی پیدا شده
    
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

    proxy = get_best_proxies()
    if proxy:
        ip, port = proxy.split(':')
        proxy_link = f"tg://socks?server={ip}&port={port}"
        
        text = (
            f"{random_emoji} **{greeting}**\n\n"
            f"✅ این {counter}اُمین پروکسی رایگان امروز است!\n"
            f"🚀 سرور با سرعت عالی و تست شده آماده اتصال است.\n\n"
            f"❤️🤍💚\n"
            f"🆔 {chat_id}\n"
            f"««««««««««««««««««««««\n\n"
            f"📢 کانال ما را به دوستان خود معرفی کنید.\n"
            f"⏰ **هر ساعت یک پروکسی جدید و رایگان ارسال می‌شود.**\n\n"
            f"🛍 جهت تهیه فیلترشکن اختصاصی (V2ray)، کلمه **«سی تو»** را به آیدی زیر ارسال 👇 نمایید:\n"
            f"👤 @vpnsito"
        )
        
        # حذف عبارت Ping Low برای ظاهر بهتر
        reply_markup = {"inline_keyboard": [[{"text": f"{random_emoji} اتصال به پروکسی {random_emoji}", "url": proxy_link}]]}
        
        payload = {
            'chat_id': chat_id,
            'text': text,
            'parse_mode': 'Markdown',
            'reply_markup': json.dumps(reply_markup),
            'disable_web_page_preview': True
        }
        
        requests.post(f"https://api.telegram.org/bot{token}/sendMessage", data=payload)
        print(f"✅ بهترین پروکسی با موفقیت ارسال شد.")
    else:
        print("❌ هیچ پروکسی سالمی در تست پینگ پیدا نشد.")

if __name__ == "__main__":
    send_proxies()
