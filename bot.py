import requests
import os
import json

token = os.getenv('BOT_TOKEN')
chat_id = os.getenv('CHAT_ID')

def send_proxies():
    print("Process Started...")
    url = "https://proxylist.geonode.com/api/proxy-list?limit=10&page=1&sort_by=lastChecked&sort_type=desc&protocols=socks5"
    
    try:
        response = requests.get(url, timeout=20)
        if response.status_code == 200:
            data = response.json()
            proxies = data.get('data', [])
            
            if proxies:
                p = proxies[0]
                ip = p['ip']
                port = p['port']
                
                proxy_link = f"tg://socks?server={ip}&port={port}"
                
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
                
                # ارسال داده‌ها به همراه دکمه شیشه‌ای
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
                print("No proxies found.")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    send_proxies()
