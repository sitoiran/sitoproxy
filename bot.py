import requests
import os
import json
import re

token = os.getenv('BOT_TOKEN')
chat_id = os.getenv('CHAT_ID')

def send_proxies():
    print("Process Started...")
    
    # منبع معتبر و مستقیم پروکسی‌های فعال تلگرام
    url = "https://raw.githubusercontent.com/Bardiafa/Telegram-Proxy-Collector/main/MTProto.txt"
    
    try:
        response = requests.get(url, timeout=20)
        if response.status_code == 200:
            text = response.text
            
            # پیدا کردن لینک‌های معتبر پروکسی تلگرام
            proxies = re.findall(r'(tg://proxy\?[^\s"\'><]+|https://t\.me/proxy\?[^\s"\'><]+)', text)
            
            if proxies:
                # انتخاب اولین پروکسی فعال لیست
                raw_link = proxies[0].strip()
                
                # استانداردسازی لینک زنده
                if raw_link.startswith("https://t.me/proxy?"):
                    proxy_link = raw_link.replace("https://t.me/proxy?", "tg://proxy?")
                else:
                    proxy_link = raw_link

                # 💡 ترفند اصلی: برای متن لینک‌دار بالا، کاراکترهای خاص رو با فرمت HTML می‌فرستیم تا مارک‌داون تلگرام خراب نشه
                link_text = f'<a href="{proxy_link}">⚡️ اتصال به پروکسی رایگان سی تو ⚡️</a>'
                
                # ساخت دکمه شیشه‌ای زیر پیام (کاملاً مشابه ساختار کد ۲ خودت)
                reply_markup = {
                    "inline_keyboard": [
                        [
                            {"text": "💎 اتصال به پروکسی 💎", "url": proxy_link}
                        ]
                    ]
                }
                
                # چیدمان متن با ساختار HTML تگ‌های ضخیم <b> جایگزین ** شده تا تداخل ایجاد نکنه
                text = (
                    f"🌍 <b>پروکسی بین‌المللی سی‌تو (سرور خارج)</b>\n\n"
                    f"{link_text}\n"
                    f"{link_text}\n"
                    f"{link_text}\n\n"
                    f"❤️🤍💚\n"
                    f"🆔 {chat_id}\n"
                    f"🆔 {chat_id}\n"
                    f"««««««««««««««««««««««\n\n"
                    f"📢 کانال ما رو به دوستان خود معرفی کنید.\n"
                    f"⏰ هر ۱ ساعت یک پروکسی جدید و رایگان ارسال می شود.\n\n"
                    f"🛍 جهت تهیه فیلترشکن اختصاصی (V2ray)، پر سرعت، بدون قطعی و در حال حاضر وصل از طریق ربات فیلترشکن سی تو ثبت سفارش کنید تا سریع تر کانفینگ و لینک ساب خود را دریافت کنید:\n"
                    f"🤖 @vpnsitobot"
                )
                
                # ارسال دقیق و ایمن داده‌ها با پایلود کد ۲ اما پارس‌مود HTML برای عبور لینک‌های طولانی
                payload = {
                    'chat_id': chat_id,
                    'text': text,
                    'parse_mode': 'HTML',
                    'reply_markup': json.dumps(reply_markup)
                }
                
                api_url = f"https://api.telegram.org/bot{token}/sendMessage"
                res = requests.post(api_url, data=payload)
                print(f"Telegram API Status: {res.status_code}")
                if res.status_code != 200:
                    print(f"Error details: {res.text}")
            else:
                print("No proxies found in source list.")
        else:
            print(f"Failed to fetch source: {response.status_code}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    send_proxies()
