import requests
import re
import json

def get_toffee_data():
    # Toffee-র মেইন লাইভ পেজ
    url = "https://toffeelive.com/en/live"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
        "Referer": "https://toffeelive.com/",
        "Accept-Language": "en-US,en;q=0.9"
    }

    print("📡 Toffee থেকে ডাটা সংগ্রহের চেষ্টা করা হচ্ছে...")
    
    try:
        # প্রথমে মেইন পেজ থেকে লেটেস্ট RSC আইডি বা ডাটা স্ট্রিম খোঁজা
        session = requests.Session()
        response = session.get(url, headers=headers, timeout=20)
        
        # যদি সরাসরি পেজে ডাটা না থাকে, তবে আপনার দেওয়া RSC লিংকটি ব্যবহার করবে
        # বর্তমানে '1dvpb' কাজ করছে, এটি পরিবর্তন হলে নিচের লিংকে আপডেট করতে হবে
        api_url = "https://toffeelive.com/en/live?_rsc=1dvpb"
        api_headers = headers.copy()
        api_headers["Rsc"] = "1"
        
        res = session.get(api_url, headers=api_headers, timeout=20)
        content = res.text

        # উন্নত রেজেক্স প্যাটার্ন
        # ১. স্ট্রিম লিংক
        streams = re.findall(r'https://[^\s"<>\\\]]+playlist\.m3u8', content)
        # ২. চ্যানেলের নাম
        titles = re.findall(r'"title":"([^"]+)"', content)
        # ৩. লোগো
        logos = re.findall(r'https://images\.toffeelive\.com/[^\s"<>\\\]]+\.png', content)

        if not streams:
            print("❌ কোনো চ্যানেল পাওয়া যায়নি। সম্ভবত আইপি ব্লক বা RSC কোড পরিবর্তন হয়েছে।")
            return

        # প্লেলিস্ট তৈরি
        m3u_file = "toffee_live.m3u"
        with open(m3u_file, "w", encoding="utf-8") as f:
            f.write("#EXTM3U\n")
            
            unique_links = set()
            count = 0
            
            for i in range(len(streams)):
                clean_url = streams[i].replace("\\u0026", "&")
                if clean_url not in unique_links:
                    name = titles[i] if i < len(titles) else f"Toffee TV {i+1}"
                    logo = logos[i] if i < len(logos) else ""
                    
                    f.write(f'#EXTINF:-1 tvg-logo="{logo}" group-title="Toffee Live", {name}\n')
                    f.write(f'#EXTVLCOPT:http-user-agent={headers["User-Agent"]}\n')
                    f.write(f'{clean_url}\n\n')
                    
                    unique_links.add(clean_url)
                    count += 1
        
        print(f"✅ সফল! {count}টি চ্যানেল প্লেলিস্টে যোগ করা হয়েছে।")

    except Exception as e:
        print(f"❌ এরর: {str(e)}")

if __name__ == "__main__":
    get_toffee_data()
