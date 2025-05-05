import os
import logging
from flask import Flask
from database import init_db
from routes_auth import auth_bp
from routes_products import products_bp
from routes_sales import sales_bp
from routes_sync import sync_bp

# Set up logging
os.makedirs('logs', exist_ok=True)
logging.basicConfig(
    filename='logs/backend.log',
    level=logging.INFO,
    format='%(asctime)s %(levelname)s: %(message)s'
)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Register blueprints
app.register_blueprint(auth_bp, url_prefix='/api')
app.register_blueprint(products_bp, url_prefix='/api')
app.register_blueprint(sales_bp, url_prefix='/api')
app.register_blueprint(sync_bp, url_prefix='/api')

# Initialize the database
try:
    print("Attempting to initialize database...")
    init_db()
    logger.info("Database initialized successfully")
    print("Database initialized successfully")
except Exception as e:
    logger.error(f"Failed to initialize database: {str(e)}")
    print(f"Failed to initialize database: {str(e)}")

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
