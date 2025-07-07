from flask import Flask, request, jsonify
import requests
import re
import os

app = Flask(__name__)

@app.route('/')
def index():
    return "Terabox Extractor API is Live"

@app.route('/terabox', methods=['POST'])
def extract_video_link():
    data = request.get_json()
    link = data.get('link')

    if not link or "terabox.com" not in link:
        return jsonify({'error': 'Invalid Terabox link'}), 400

    try:
        # Extract file code from the link
        match = re.search(r'surl=([a-zA-Z0-9_-]+)', link)
        if not match:
            return jsonify({'error': 'Invalid link format'}), 400

        surl = match.group(1)
        share_url = f'https://www.terabox.com/share/list?app_id=250528&shorturl={surl}&root=1'

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
            'Referer': link
        }

        response = requests.get(share_url, headers=headers)
        json_data = response.json()

        if 'list' not in json_data or not json_data['list']:
            return jsonify({'error': 'File list not found'}), 404

        file_info = json_data['list'][0]
        fs_id = file_info['fs_id']

        # Get direct download link
        dlink_api = f'https://www.terabox.com/share/download?app_id=250528&shorturl={surl}&fs_id={fs_id}'
        download_response = requests.get(dlink_api, headers=headers)
        if download_response.status_code != 200:
            return jsonify({'error': 'Failed to fetch download link'}), 500

        video_link = re.search(r'https://download[^"]+\.mp4', download_response.text)
        if not video_link:
            return jsonify({'error': 'Video link not found'}), 404

        return jsonify({
            'title': file_info.get('server_filename', 'Terabox Video'),
            'qualities': {
                'Auto': video_link.group(0)
            },
            'isPremium': False
        })

    except Exception as e:
        return jsonify({'error': f'Exception occurred: {str(e)}'}), 500


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
