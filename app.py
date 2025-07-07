from flask import Flask, request, jsonify
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import re

app = Flask(__name__)

@app.route('/terabox', methods=['POST'])
def get_terabox_link():
    data = request.get_json()
    share_url = data.get('link')

    if not share_url or not share_url.startswith('http'):
        return jsonify({'error': 'Invalid link'}), 400

    try:
        # Headless Chrome options
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")

        # Start Chrome
        driver = webdriver.Chrome(options=chrome_options)
        driver.get(share_url)

        # Wait for the page to load
        WebDriverWait(driver, 15).until(
            lambda d: "download" in d.page_source
        )

        page_source = driver.page_source
        title = driver.title or 'Terabox Video'

        # Extract .mp4 download link
        match = re.search(r'https://download[^"]+\.mp4', page_source)
        dlink = match.group(0) if match else None

        driver.quit()

        if not dlink:
            return jsonify({'error': 'Video link not found'}), 404

        return jsonify({
            'title': title,
            'qualities': {
                'Auto': dlink
            },
            'isPremium': False
        })

    except Exception as e:
        return jsonify({'error': f'Exception occurred: {str(e)}'}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
