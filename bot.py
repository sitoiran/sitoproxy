import requests
import os

token = os.getenv('BOT_TOKEN')
chat_id = os.getenv('CHAT_ID')

def send_proxies():
    print("Process Started...")
    # منبع جایگزین که فیلتر نیست و به گیت‌هاب پاسخ می‌دهد
    url = "https://raw.githubusercontent.com/hookzof/socks5_list/master/tg.txt"
    
    try:
        print("Fetching proxies from a stable global source...")
        response = requests.get(url, timeout=20)
        
        if response.status_code == 200:
            # جدا کردن خطوط و پیدا کردن لینک‌های سالم
            proxies = [l.strip() for l in response.text.split('\n') if 't.me/proxy?proxy=' in l]
            
            if proxies:
                # ارسال فقط ۱ عدد پروکسی (طبق درخواستت)
                proxy = proxies[0]
                text = f"🌍 **پروکسی بین‌المللی سی‌تو (ضد فیلتر)**\n\n🔗 {proxy}\n\n🆔 {chat_id}"
                
                api_url = f"https://api.telegram.org/bot{token}/sendMessage"
                res = requests.post(api_url, data={'chat_id': chat_id, 'text': text})
                
                if res.status_code == 200:
                    print("✅ پیام با موفقیت به تلگرام ارسال شد!")
                else:
                    print(f"❌ Telegram Error: {res.text}")
            else:
                print("No valid proxies found in source.")
        else:
            print(f"❌ Source Error: {response.status_code}")
            
    except Exception as e:
        print(f"⚠️ Critical Error: {e}")

if __name__ == "__main__":
    send_proxies()
