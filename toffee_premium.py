import requests
import re
import os

def generate_toffee_playlist():
    # আপনার স্ক্রিনশট অনুযায়ী Next.js রেন্ডার রিকোয়েস্ট ইউআরএল
    target_url = "https://toffeelive.com/en/live?_rsc=1dvpb"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
        "Referer": "https://toffeelive.com/en/live",
        "Rsc": "1",
        "Accept": "*/*"
    }

    print("📡 Toffee থেকে ডাটা সংগ্রহ করা হচ্ছে...")
    
    try:
        response = requests.get(target_url, headers=headers, timeout=20)
        response.raise_for_status()
        raw_data = response.text

        # Regex ব্যবহার করে চ্যানেলের নাম, লোগো এবং স্ট্রিম ইউআরএল বের করা
        # Toffee-র ডাটা ফরম্যাট অনুযায়ী এই প্যাটার্নগুলো কাজ করবে
        stream_pattern = r'https://[^\s"<>]+playlist\.m3u8'
        logo_pattern = r'https://images\.toffeelive\.com/[^\s"<>]+logo[^\s"<>]+\.png'
        title_pattern = r'"title":"([^"]+)"'

        streams = re.findall(stream_pattern, raw_data)
        logos = re.findall(logo_pattern, raw_data)
        titles = re.findall(title_pattern, raw_data)

        # ডুপ্লিকেট ইউআরএল পরিষ্কার করা
        unique_channels = []
        seen_urls = set()

        for i in range(len(streams)):
            url = streams[i].replace("\\u0026", "&")
            if url not in seen_urls:
                name = titles[i] if i < len(titles) else f"Toffee Channel {i+1}"
                logo = logos[i] if i < len(logos) else ""
                unique_channels.append({"name": name, "url": url, "logo": logo})
                seen_urls.add(url)

        # M3U ফাইল তৈরি
        m3u_file = "toffee_live.m3u"
        with open(m3u_file, "w", encoding='utf-8') as f:
            f.write("#EXTM3U\n")
            for ch in unique_channels:
                f.write(f'#EXTINF:-1 tvg-id="{ch["name"]}" tvg-logo="{ch["logo"]}" group-title="Toffee Live", {ch["name"]}\n')
                # কুকি এবং ইউজার এজেন্ট হেডার যোগ করা (প্লেয়ারের জন্য)
                f.write(f'#EXTVLCOPT:http-user-agent={headers["User-Agent"]}\n')
                f.write(f'{ch["url"]}\n\n')

        print(f"✅ সফলভাবে {len(unique_channels)}টি চ্যানেলসহ প্লেলিস্ট তৈরি হয়েছে: {m3u_file}")

    except Exception as e:
        print(f"❌ ভুল হয়েছে: {str(e)}")

if __name__ == "__main__":
    generate_toffee_playlist()
