FROM python:3.11-slim

WORKDIR /app

# Install minimal required packages (no Chrome)
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["python", "app.py"]
