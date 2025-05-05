FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy Python files from root
COPY app.py .
COPY database.py .
COPY models.py .
COPY main.py .
COPY routes_auth.py .
COPY routes_products.py .
COPY routes_sales.py .
COPY routes_sync.py .
COPY ui_login.py .
COPY ui_products.py .
COPY ui_sales.py .
COPY ui_settings.py .
COPY utils_network.py .

# Ensure logs directory and permissions
RUN mkdir -p /app/logs && chmod -R 777 /app/logs

# Debug: List directory structure
RUN ls -R /app

EXPOSE 5000 8000

CMD ["sh", "-c", "python app.py & sleep 5 && python main.py"]
