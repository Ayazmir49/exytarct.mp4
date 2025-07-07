from flask import Flask, request, jsonify
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re
import time
import os

app = Flask(__name__)

@app.route('/')
def home():
    return 'Terabox Extractor API is running.'

@app.route('/terabox', methods=['POST'])
def get_terabox_link():
    data = request.get_json()
    share_url = data.get('link')

    if not share_url or not share_url.startswith('http'):
        return jsonify({'error': 'Invalid link'}), 400

    try:
        # Setup Chrome options for headless browser
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")

        # Setup Chrome driver
        driver = webdriver.Chrome(options=chrome_options)

        # Open the shared Terabox link
        driver.get(share_url)

        print("Opened URL:", share_url)

        # Wait for up to 20 seconds until the video tag or download link appears
        WebDriverWait(driver, 20).until(
            lambda d: ".mp4" in d.page_source
        )

        page_source = driver.page_source
        title = driver.title or 'Terabox Video'

        print("Page loaded. Looking for .mp4 link...")

        # Extract .mp4 download link using regex
        match = re.search(r'https://[^"]+\.mp4[^"]*', page_source)
        dlink = match.group(0) if match else None

        driver.quit()

        if not dlink:
            print("No .mp4 link found.")
            return jsonify({'error': 'Video link not found'}), 404

        print("Video link found:", dlink)

        return jsonify({
            'title': title,
            'qualities': {
                'Auto': dlink
            },
            'isPremium': False
        })

    except Exception as e:
        print("Exception occurred:", str(e))
        return jsonify({'error': f'Exception occurred: {str(e)}'}), 500


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
