FROM python:3.11-slim

RUN apt-get update && apt-get install -y wget curl gnupg     libnss3 libatk-bridge2.0-0 libxss1 libasound2 libxcomposite1     libxdamage1 libxrandr2 libgtk-3-0 libgbm1 libxshmfence1     libx11-xcb1 libxcb-dri3-0 libdrm2 libxfixes3 libxext6 libx11-6 libgl1     && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY . /app

RUN pip install --no-cache-dir -r requirements.txt && playwright install --with-deps

CMD ["python", "main.py"]
