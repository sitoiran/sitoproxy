import requests
import os

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
                
                # متن نهایی با چیدمان قلب‌ها و جابه‌جایی ایموجی اشاره
                text = (
                    f"🌍 **پروکسی بین‌المللی سی‌تو (سرور خارج)**\n\n"
                    f"🔗 {proxy_link}\n\n"
                    f"❤️🤍💚\n"
                    f"🆔 {chat_id}\n"
                    f"🆔 {chat_id}\n"
                    f"««««««««««««««««««««««\n\n"
                    f"📢 کانال ما رو به دوستان خود معرفی کنید.\n"
                    f"⏰ هر ۳۰ دقیقه یک پروکسی جدید و رایگان ارسال می شود.\n\n"
                    f"🛍 جهت تهیه فیلترشکن اختصاصی (V2ray)، پر سرعت، بدون قطعی و در حال حاضر وصل کلمه **«سی تو»** را به آیدی زیر ارسال 👇 نمایید:\n"
                    f"👤 @vpnsito"
                )
                
                api_url = f"https://api.telegram.org/bot{token}/sendMessage"
                res = requests.post(api_url, data={'chat_id': chat_id, 'text': text, 'parse_mode': 'Markdown'})
                print(f"Telegram API Status: {res.status_code}")
            else:
                print("No proxies found.")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    send_proxies()
