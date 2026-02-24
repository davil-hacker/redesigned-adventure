import requests
import json
import os
from datetime import datetime

def get_toffee_cookies():
    # Toffee-র API এন্ডপয়েন্ট যেখান থেকে ডাইনামিক ডাটা আসে
    api_url = "https://toffeelive.com/en/live?_rsc=1dvpb"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
        "Referer": "https://toffeelive.com/en/live",
        "Rsc": "1"
    }

    try:
        response = requests.get(api_url, headers=headers, timeout=20)
        raw_content = response.text
        
        # আপনার দেওয়া স্ট্রাকচার অনুযায়ী ডাটা প্রসেস করার ফাংশন
        # এখানে আমরা ডাইনামিক কুকি এবং লিংকগুলো এক্সট্রাক্ট করব
        import re
        links = re.findall(r'https://[^\s"<>\\\]]+playlist\.m3u8', raw_content)
        cookies = re.findall(r'Edge-Cache-Cookie=[^"\s\\\]]+', raw_content)
        titles = re.findall(r'"title":"([^"]+)"', raw_content)
        logos = re.findall(r'https://assets-prod\.services\.toffeelive\.com/[^\s"<>\\\]]+\.png', raw_content)

        updated_data = []
        unique_links = set()

        for i in range(len(links)):
            clean_link = links[i].replace("\\u0026", "&")
            if clean_link not in unique_links:
                channel_info = {
                    "id": f"channel_{i}",
                    "name": titles[i] if i < len(titles) else "Toffee Channel",
                    "logo": logos[i] if i < len(logos) else "",
                    "link": clean_link,
                    "cookie": cookies[i] if i < len(cookies) else ""
                }
                updated_data.append(channel_info)
                unique_links.add(clean_link)

        # JSON ফাইল সেভ করা
        with open("toffee.json", "w", encoding='utf-8') as f:
            json.dump(updated_data, f, indent=2)

        # M3U ফাইল তৈরি (প্লেয়ারে দেখার জন্য)
        with open("toffee.m3u", "w", encoding='utf-8') as f:
            f.write("#EXTM3U\n")
            for ch in updated_data:
                f.write(f'#EXTINF:-1 tvg-logo="{ch["logo"]}", {ch["name"]}\n')
                f.write(f'#EXTVLCOPT:http-user-agent={headers["User-Agent"]}\n')
                f.write(f'#EXTVLCOPT:http-referrer=https://toffeelive.com/\n')
                f.write(f'#EXTVLCOPT:http-cookie={ch["cookie"]}\n')
                f.write(f'{ch["link"]}\n\n')

        print(f"✅ Cookies Updated at {datetime.now()}")
        return True
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    get_toffee_cookies()
