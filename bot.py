import requests
import os
import re
import json

token = os.getenv('BOT_TOKEN')
chat_id = os.getenv('CHAT_ID')

def get_best_proxies():
    sources = [
        "https://raw.githubusercontent.com/hookzof/socks5_list/master/proxy.txt",
        "https://api.proxyscrape.com/v2/?request=displayproxies&protocol=socks5&timeout=10000&country=all&ssl=all&anonymity=all",
        "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/socks5.txt"
    ]
    
    for url in sources:
        try:
            response = requests.get(url, timeout=15)
            if response.status_code == 200:
                proxies = re.findall(r'\d+\.\d+\.\d+\.\d+:\d+', response.text)
                if proxies:
                    return proxies[0] 
        except:
            continue
    return None

def send_proxies():
    print("🚀 در حال جستجوی پروکسی جدید سی‌تو...")
    
    proxy = get_best_proxies()
    
    if proxy:
        ip, port = proxy.split(':')
        proxy_link = f"tg://socks?server={ip}&port={port}"
        
        # متن پیام (بدون لینک‌های شلوغ داخل متن)
        text = (
            f"🌍 **پروکسی بین‌المللی سی‌تو (ویژه عبور از فیلترینگ)**\n\n"
            f"✅ سرور با سرعت عالی و تست شده آماده اتصال است.\n\n"
            f"❤️🤍💚\n"
            f"🆔 {chat_id}\n"
            f"««««««««««««««««««««««\n\n"
            f"📢 کانال ما را به دوستان خود معرفی کنید.\n"
            f"⏰ **هر ساعت یک پروکسی جدید و رایگان ارسال می‌شود.**\n\n"
            f"🛍 جهت تهیه فیلترشکن اختصاصی (V2ray)، پر سرعت و بدون قطعی، کلمه **«سی تو»** را به آیدی زیر ارسال 👇 نمایید:\n"
            f"👤 @vpnsito"
        )
        
        # ساخت دکمه شیشه‌ای
        reply_markup = {
            "inline_keyboard": [
                [
                    {"text": "⚡️ اتصال به پروکسی ⚡️", "url": proxy_link}
                ]
            ]
        }
        
        api_url = f"https://api.telegram.org/bot{token}/sendMessage"
        payload = {
            'chat_id': chat_id,
            'text': text,
            'parse_mode': 'Markdown',
            'reply_markup': json.dumps(reply_markup) # تبدیل دکمه به فرمت JSON
        }
        
        res = requests.post(api_url, data=payload)
        print(f"✅ وضعیت ارسال: {res.status_code}")
    else:
        print("❌ پروکسی پیدا نشد.")

if __name__ == "__main__":
    send_proxies()
