FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app/__init__.py .
COPY app/backend/__init__.py backend/__init__.py
COPY app/backend/app.py backend/app.py
COPY app/db/__init__.py db/__init__.py
COPY app/db/database.py db/database.py
COPY app/db/models.py db/models.py
COPY app/frontend/__init__.py frontend/__init__.py
COPY app/frontend/main.py frontend/main.py
COPY app/utils/__init__.py utils/__init__.py
COPY app/config/__init__.py config/__init__.py

EXPOSE 5000 8000

CMD ["sh", "-c", "python backend/app.py & python frontend/main.py --web --port 8000"]
