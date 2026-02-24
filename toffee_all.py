import requests
import re
import os
from datetime import datetime

def fetch_toffee_all():
    # Toffee-র মেইন ক্যাটাগরিগুলো
    categories = ['sports', 'entertainment', 'news', 'cinema']
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
        "Referer": "https://toffeelive.com/en/live",
        "Rsc": "1" # Next.js ডাটা পাওয়ার জন্য জরুরি
    }

    all_channels = []
    seen_urls = set()

    print("🚀 All channels fetch করা শুরু হচ্ছে...")

    for cat in categories:
        # RSC ইউআরএল (1dvpb কোডটি কাজ না করলে ব্রাউজার থেকে আপডেট করে নিন)
        url = f"https://toffeelive.com/en/categories/{cat}?_rsc=1dvpb"
        
        try:
            print(f"📡 ক্যাটাগরি স্ক্যান হচ্ছে: {cat.upper()}")
            response = requests.get(url, headers=headers, timeout=20)
            content = response.text

            # Regex দিয়ে ডাটা খোঁজা
            # ১. m3u8 স্ট্রিম লিংক
            streams = re.findall(r'https://[^\s"<>\\\]]+playlist\.m3u8', content)
            # ২. চ্যানেলের নাম
            titles = re.findall(r'"title":"([^"]+)"', content)
            # ৩. চ্যানেলের লোগো
            logos = re.findall(r'https://images\.toffeelive\.com/[^\s"<>\\\]]+\.png', content)

            for i in range(len(streams)):
                clean_url = streams[i].replace("\\u0026", "&")
                if clean_url not in seen_urls:
                    name = titles[i] if i < len(titles) else f"{cat.capitalize()} Ch {i+1}"
                    logo = logos[i] if i < len(logos) else ""
                    
                    all_channels.append({
                        "name": name,
                        "url": clean_url,
                        "logo": logo,
                        "category": cat.capitalize()
                    })
                    seen_urls.add(clean_url)

        except Exception as e:
            print(f"❌ {cat} ক্যাটাগরিতে এরর: {e}")

    # M3U ফাইল তৈরি
    if all_channels:
        m3u_file = "toffee_all.m3u"
        with open(m3u_file, "w", encoding='utf-8') as f:
            f.write("#EXTM3U\n")
            for ch in all_channels:
                f.write(f'#EXTINF:-1 tvg-logo="{ch["logo"]}" group-title="{ch["category"]}", {ch["name"]}\n')
                f.write(f'#EXTVLCOPT:http-user-agent={headers["User-Agent"]}\n')
                f.write(f'{ch["url"]}\n\n')
        
        print(f"✅ সফল! মোট {len(all_channels)}টি চ্যানেল পাওয়া গেছে।")
    else:
        print("❌ কোনো চ্যানেল পাওয়া যায়নি। হয়তো আইপি ব্লক করা হয়েছে।")

if __name__ == "__main__":
    fetch_toffee_all()
