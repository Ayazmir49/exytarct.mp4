#!/bin/bash
# Start Chrome driver in background
/opt/google/chrome/chrome --headless --no-sandbox --disable-dev-shm-usage --remote-debugging-port=9222 &
# Start the Flask app
python3 app.py
