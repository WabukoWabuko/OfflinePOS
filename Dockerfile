FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy Python files from root
COPY app.py .
COPY database.py .
COPY models.py .
COPY main.py .

# Ensure logs directory and permissions
RUN mkdir -p /app/logs && chmod -R 777 /app/logs

# Debug: List directory structure
RUN ls -R /app

EXPOSE 5000 8000

CMD ["sh", "-c", "python app.py & python main.py"]
