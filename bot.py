import requests
import os
import re

token = os.getenv('BOT_TOKEN')
chat_id = os.getenv('CHAT_ID')

def get_best_proxies():
    # منابعی که پروکسی‌های سالم و تازه را برای عبور از محدودیت آپدیت می‌کنند
    sources = [
        "https://raw.githubusercontent.com/hookzof/socks5_list/master/proxy.txt",
        "https://api.proxyscrape.com/v2/?request=displayproxies&protocol=socks5&timeout=10000&country=all&ssl=all&anonymity=all",
        "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/socks5.txt"
    ]
    
    for url in sources:
        try:
            response = requests.get(url, timeout=15)
            if response.status_code == 200:
                # استخراج آی‌پی و پورت
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
        # ساخت لینک استاندارد SOCKS5 تلگرام
        proxy_link = f"tg://socks?server={ip}&port={port}"
        
        text = (
            f"🌍 **پروکسی بین‌المللی سی‌تو (ویژه عبور از فیلترینگ)**\n\n"
            f"🔗 `{proxy_link}`\n\n"
            f"☝️ **روی لینک بالا بزنید تا متصل شوید**\n\n"
            f"❤️🤍💚\n"
            f"🆔 {chat_id}\n"
            f"««««««««««««««««««««««\n\n"
            f"📢 کانال ما را به دوستان خود معرفی کنید.\n"
            f"⏰ **هر ساعت یک پروکسی جدید و رایگان ارسال می‌شود.**\n\n"
            f"🛍 جهت تهیه فیلترشکن اختصاصی (V2ray)، پر سرعت و بدون قطعی، کلمه **«سی تو»** را به آیدی زیر ارسال 👇 نمایید:\n"
            f"👤 @vpnsito"
        )
        
        api_url = f"https://api.telegram.org/bot{token}/sendMessage"
        payload = {
            'chat_id': chat_id,
            'text': text,
            'parse_mode': 'Markdown'
        }
        
        res = requests.post(api_url, data=payload)
        print(f"✅ وضعیت ارسال: {res.status_code}")
    else:
        print("❌ پروکسی پیدا نشد.")

if __name__ == "__main__":
    send_proxies()
