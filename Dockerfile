FROM python:slim

WORKDIR /app

COPY requirements.txt .

RUN apt update -y && \
    apt install -y curl && \
    pip install --no-cache-dir -r requirements.txt && \
    apt clean && \
    rm -rf /var/lib/apt/lists/*

COPY . .

EXPOSE 3005

RUN chmod +x main.py

CMD ["python", "main.py"]
