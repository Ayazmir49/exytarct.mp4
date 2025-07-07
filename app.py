from flask import Flask, request, jsonify
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import re
import os

app = Flask(__name__)

@app.route('/terabox', methods=['POST'])
def get_terabox_link():
    data = request.get_json()
    share_url = data.get('link')

    if not share_url or not share_url.startswith('http'):
        return jsonify({'error': 'Invalid or missing link'}), 400

    try:
        # Chrome options for headless browsing
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")

        # ChromeDriver path (env var fallback)
        chromedriver_path = os.getenv("CHROMEDRIVER_PATH", "chromedriver")
        service = Service(chromedriver_path)
        driver = webdriver.Chrome(service=service, options=chrome_options)

        # Load the shared Terabox link
        driver.get(share_url)

        # Wait for the page to load and video content to appear
        WebDriverWait(driver, 20).until(
            lambda d: "download" in d.page_source or ".mp4" in d.page_source
        )

        page_source = driver.page_source
        title = driver.title or 'Terabox Video'

        # Try to extract .mp4 link via regex
        match = re.search(r'https://download[^"]+\.mp4', page_source, re.IGNORECASE)
        dlink = match.group(0) if match else None

        driver.quit()

        if not dlink:
            return jsonify({'error': 'Video link not found'}), 404

        return jsonify({
            'title': title,
            'qualities': {
                'Auto': dlink
            },
            'isPremium': False,
            'source': share_url
        })

    except Exception as e:
        try:
            driver.quit()
        except:
            pass
        return jsonify({'error': f'Exception occurred: {str(e)}'}), 500


if __name__ == '__main__':
    app.run(debug=True)
