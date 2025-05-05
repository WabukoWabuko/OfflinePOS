FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy all app subdirectories explicitly
COPY app/__init__.py .
COPY app/backend/ backend/
COPY app/db/ db/
COPY app/frontend/ frontend/
COPY app/utils/ utils/
COPY app/config/ config/

# Debug: List directory structure
RUN ls -R /app

EXPOSE 5000 8000

CMD ["sh", "-c", "python backend/app.py & python frontend/main.py"]
