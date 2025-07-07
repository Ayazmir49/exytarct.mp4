FROM python:3.11-slim

WORKDIR /app

# Install required system packages for Chrome and Selenium
RUN apt-get update && apt-get install -y \
    wget gnupg unzip curl fonts-liberation \
    libasound2 libatk1.0-0 libatk-bridge2.0-0 \
    libcups2 libdbus-1-3 libgdk-pixbuf2.0-0 \
    libnspr4 libnss3 libx11-xcb1 libxcomposite1 \
    libxdamage1 libxrandr2 xdg-utils libgbm1 libgtk-3-0 \
    chromium chromium-driver && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["python", "app.py"]
