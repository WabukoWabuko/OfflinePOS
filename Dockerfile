FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app/ .

EXPOSE 5000 8000

CMD ["sh", "-c", "python backend/app.py & python frontend/main.py --web --port 8000"]
