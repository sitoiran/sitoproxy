import requests
import os

token = os.getenv('BOT_TOKEN')
chat_id = os.getenv('CHAT_ID')

# منبع بین‌المللی بسیار معتبر که مدام آپدیت می‌شود
source_url = "https://raw.githubusercontent.com/hookzof/socks5_list/master/tg.txt"

def send_proxies():
    print("Connecting to Global Proxy Source...")
    try:
        # استفاده از Timeout برای جلوگیری از گیر کردن در شبکه
        response = requests.get(source_url, timeout=30)
        
        if response.status_code == 200:
            # جدا کردن لینک‌ها
            lines = response.text.split('\n')
            proxies = [l.strip() for l in lines if 't.me/proxy?proxy=' in l]
            
            if not proxies:
                print("No proxies found in the list. Checking formatting...")
                proxies = [l.strip() for l in lines if len(l) > 10]

            print(f"Found {len(proxies)} global proxies. Sending top 3...")
            
            count = 0
            for proxy_link in proxies[:3]:
                # آماده‌سازی متن پیام
                text = f"🌍 **پروکسی بین‌المللی سی‌تو (بدون قطعی)**\n\n🔗 {proxy_link}\n\n🆔 {chat_id}"
                
                url = f"https://api.telegram.org/bot{token}/sendMessage"
                res = requests.post(url, data={'chat_id': chat_id, 'text': text, 'parse_mode': 'Markdown'})
                
                print(f"Proxy {count+1} Status: {res.status_code} - {res.text}")
                count += 1
                
            if count == 0:
                print("Success fetching source, but no valid links extracted.")
        else:
            print(f"Source Error: {response.status_code} - Could not reach the server.")
            
    except Exception as e:
        print(f"System Error: {e}")

if __name__ == "__main__":
    send_proxies()
