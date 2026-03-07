import requests
import os

token = os.getenv('BOT_TOKEN')
chat_id = os.getenv('CHAT_ID')

def send_proxies():
    print("Process Started...")
    # استفاده از یک منبع جایگزین که فایل متنی نیست (API مستقیم)
    # این آدرس معمولاً توسط گیت‌هاب مسدود نمی‌شود
    url = "https://proxylist.geonode.com/api/proxy-list?limit=10&page=1&sort_by=lastChecked&sort_type=desc&protocols=socks5"
    
    try:
        print("Fetching fresh SOCKS5/MTProto data...")
        response = requests.get(url, timeout=20)
        
        if response.status_code == 200:
            data = response.json()
            proxies = data.get('data', [])
            
            if proxies:
                # گرفتن مشخصات اولین سرور (مثلاً آلمان یا آمریکا)
                p = proxies[0]
                ip = p['ip']
                port = p['port']
                
                # تبدیل به فرمت پروکسی تلگرام (MTProto پیشنهادی)
                # اگر سرور مخصوص داری جایگزین کن، در غیر این صورت پیام تست می‌فرستیم
                proxy_link = f"tg://socks?server={ip}&port={port}"
                
                text = f"🌍 **پروکسی بین‌المللی سی‌تو (سرور خارج)**\n\n🔗 {proxy_link}\n\n🆔 {chat_id}"
                
                api_url = f"https://api.telegram.org/bot{token}/sendMessage"
                res = requests.post(api_url, data={'chat_id': chat_id, 'text': text})
                
                print(f"Telegram API Status: {res.status_code}")
            else:
                print("No proxies found in API response.")
        else:
            print(f"Source Error: {response.status_code} - Switching to Emergency Message")
            # اگر باز هم منبع قطع بود، حداقل بفهمیم ربات کار می‌کند:
            requests.post(f"https://api.telegram.org/bot{token}/sendMessage", 
                          data={'chat_id': chat_id, 'text': "🤖 ربات آنلاین است اما منابع پروکسی مسدود هستند. در حال بررسی منبع جدید..."})

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    send_proxies()
