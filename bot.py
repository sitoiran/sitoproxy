import requests
import os

token = os.getenv('BOT_TOKEN')
chat_id = os.getenv('CHAT_ID')

# لیست منابع مختلف (اگه یکی ۴۰۴ داد، بره سراغ بعدی)
sources = [
    "https://api.proxyscrape.com/v2/?request=displayproxies&protocol=socks5&timeout=10000&country=all",
    "https://raw.githubusercontent.com/hookzof/socks5_list/master/tg.txt",
    "https://raw.githubusercontent.com/jetkai/proxy-list/main/online-proxies/txt/proxies-socks5.txt"
]

def send_proxies():
    print("Searching for proxies in multiple sources...")
    found_proxies = []
    
    for url in sources:
        try:
            print(f"Testing source: {url}")
            res = requests.get(url, timeout=15)
            if res.status_code == 200:
                lines = res.text.split('\n')
                # استخراج لینک‌های پروکسی تلگرام
                valid = [l.strip() for l in lines if 't.me/proxy?proxy=' in l or (len(l) > 20 and ':' in l)]
                if valid:
                    found_proxies.extend(valid)
                    print(f"Found {len(valid)} proxies here!")
                    break # اگه پیدا کرد دیگه بقیه رو نچرخه
        except:
            continue

    if found_proxies:
        count = 0
        for p in found_proxies[:3]:
            # اگه لینک تلگرامی نبود، به فرمت تلگرام تبدیلش کن
            link = p if 't.me' in p else f"https://t.me/proxy?proxy={p}"
            text = f"🚀 **پروکسی جدید سی‌تو**\n\n🔗 {link}\n\n🆔 {chat_id}"
            url = f"https://api.telegram.org/bot{token}/sendMessage"
            requests.post(url, data={'chat_id': chat_id, 'text': text})
            count += 1
        print(f"Successfully sent {count} proxies to {chat_id}")
    else:
        print("All sources failed or returned 404. Let's send a test message instead.")
        # برای اینکه بفهمی ربات سالمه، این پیام رو می‌فرسته:
        requests.post(f"https://api.telegram.org/bot{token}/sendMessage", 
                      data={'chat_id': chat_id, 'text': "🤖 ربات فعال است اما منبع پروکسی پیدا نشد."})

if __name__ == "__main__":
    send_proxies()
