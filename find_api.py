import os
from seleniumwire import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time

def find_toffee_api():
    chrome_options = Options()
    chrome_options.add_argument("--headless") # ডিসপ্লে ছাড়া রান হবে
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    
    # ব্রাউজার সেটআপ
    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=chrome_options
    )

    print("Targeting Toffee...")
    driver.get("https://toffeelive.com/en/live")
    time.sleep(15) # পেজ লোড হওয়ার জন্য সময়

    # ডাটা খুঁজে বের করা
    found_urls = []
    for request in driver.requests:
        if request.response:
            url = request.url
            if 'api' in url or 'm3u8' in url or 'get-token' in url:
                found_urls.append(url)
                print(f"Found: {url}")

    # রেজাল্ট একটি ফাইলে সেভ করা যাতে আপনি GitHub থেকে দেখতে পারেন
    with open("found_apis.txt", "w") as f:
        for link in found_urls:
            f.write(link + "\n")

    driver.quit()

if __name__ == "__main__":
    find_toffee_api()
