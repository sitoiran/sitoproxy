import requests
import os

token = os.getenv('BOT_TOKEN')
chat_id = os.getenv('CHAT_ID')

def send_proxies():
    print("Process Started...")
    # این منبع یک API است که همیشه پروکسی‌های تازه تولید می‌کند
    url = "https://mtpro.xyz/api/?type=mtproto"
    
    try:
        print(f"Connecting to API...")
        response = requests.get(url, timeout=20)
        
        if response.status_code == 200:
            data = response.json() # خروجی این سایت JSON است
            print("Data received successfully!")
            
            if len(data) > 0:
                # گرفتن اولین پروکسی از لیست
                p = data[0]
                server = p.get('server')
                port = p.get('port')
                secret = p.get('secret')
                
                # ساخت لینک استاندارد
                proxy_link = f"https://t.me/proxy?server={server}&port={port}&secret={secret}"
                
                msg = f"🚀 **پروکسی جدید و اختصاصی سی‌تو**\n\n🔗 {proxy_link}\n\n🆔 {chat_id}"
                api_url = f"https://api.telegram.org/bot{token}/sendMessage"
                res = requests.post(api_url, data={'chat_id': chat_id, 'text': msg, 'parse_mode': 'Markdown'})
                print(f"Telegram Response: {res.status_code}")
            else:
                print("API returned empty list.")
        else:
            print(f"API Error: {response.status_code}")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    send_proxies()
