import requests
import os

token = os.getenv('BOT_TOKEN')
chat_id = os.getenv('CHAT_ID')

# استفاده از یک منبع کاملاً متفاوت و معتبر (API پروکسی‌های تلگرام)
source_url = "https://mtpro.xyz/api/?type=mtproto"

def send_proxies():
    print("Connecting to International Proxy API...")
    try:
        # دریافت داده‌ها از API
        response = requests.get(source_url, timeout=25)
        
        if response.status_code == 200:
            data = response.json() # این منبع خروجی JSON می‌دهد که خیلی پایدارتر است
            
            print(f"Successfully connected. Sending proxies...")
            
            count = 0
            # پیمایش در لیست پروکسی‌های دریافت شده
            for item in data[:3]: # گرفتن ۳ تای اول
                server = item.get('server')
                port = item.get('port')
                secret = item.get('secret')
                
                # ساختن لینک استاندارد تلگرام
                proxy_link = f"https://t.me/proxy?server={server}&port={port}&secret={secret}"
                
                text = f"🌍 **پروکسی بین‌المللی سی‌تو (سرور خارج)**\n\n🔗 {proxy_link}\n\n🆔 {chat_id}"
                
                url = f"https://api.telegram.org/bot{token}/sendMessage"
                res = requests.post(url, data={'chat_id': chat_id, 'text': text, 'parse_mode': 'Markdown'})
                
                print(f"Proxy {count+1} Status: {res.status_code}")
                count += 1
        else:
            print(f"API Error: {response.status_code}. Trying backup source...")
            # اگر اولی نشد، یک منبع ساده‌تر را امتحان کن
            backup_res = requests.get("https://raw.githubusercontent.com/bikulov/proxylist/master/proxylist.txt")
            print(f"Backup Source Status: {backup_res.status_code}")

    except Exception as e:
        print(f"Critical System Error: {e}")

if __name__ == "__main__":
    send_proxies()
