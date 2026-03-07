import requests
import os

token = os.getenv('BOT_TOKEN')
chat_id = os.getenv('CHAT_ID')

# منبع جایگزین که سرعت بسیار بالایی دارد
source_url = "https://raw.githubusercontent.com/skfhw/mtproxy/main/proxies.txt"

def send_proxies():
    print("Connecting to Fast Source...")
    try:
        # تنظیم تایم‌اوت روی 10 ثانیه که زرد نماند
        response = requests.get(source_url, timeout=10)
        
        if response.status_code == 200:
            lines = response.text.split('\n')
            # فیلتر کردن لینک‌های معتبر
            proxies = [l.strip() for l in lines if 't.me/proxy?proxy=' in l]
            
            print(f"Found {len(proxies)} proxies. Sending...")
            
            count = 0
            for proxy_link in proxies[:3]:
                text = f"🚀 **پروکسی جدید سی‌تو**\n\n🔗 {proxy_link}\n\n🆔 {chat_id}"
                url = f"https://api.telegram.org/bot{token}/sendMessage"
                res = requests.post(url, data={'chat_id': chat_id, 'text': text})
                print(f"Sent {count+1}: {res.status_code}")
                count += 1
        else:
            print(f"Failed with status: {response.status_code}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    send_proxies()
