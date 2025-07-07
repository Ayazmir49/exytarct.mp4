FROM python:3.10-slim

# Install dependencies
RUN apt-get update && apt-get install -y \
    wget curl unzip gnupg2 \
    chromium chromium-driver \
    && rm -rf /var/lib/apt/lists/*

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV CHROMEDRIVER_PATH=/usr/bin/chromedriver

# Create app directory
WORKDIR /app

# Copy files
COPY . /app
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy entrypoint
RUN chmod +x /app/entrypoint.sh

EXPOSE 5000
CMD ["/app/entrypoint.sh"]
