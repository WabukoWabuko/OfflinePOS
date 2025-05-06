from flask import Flask
from routes_auth import auth_bp
from routes_products import products_bp
from routes_sales import sales_bp
from routes_sync import sync_bp
from routes_customers import customers_bp
from database import Base, engine, SessionLocal
import os
import logging

# Setup logging
logging.basicConfig(level=logging.INFO, filename='/app/logs/backend.log', filemode='a',
                    format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Register blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(products_bp)
app.register_blueprint(sales_bp)
app.register_blueprint(sync_bp)
app.register_blueprint(customers_bp)

# Flag to ensure initialization happens only once
db_initialized = False

def init_db():
    global db_initialized
    if not db_initialized:
        logger.info("Attempting to initialize database...")
        file_exists = os.path.exists("/app/offline_pos.db")
        logger.info(f"Database file exists: {file_exists}")
        if not file_exists:
            logger.info("Creating database tables...")
            Base.metadata.create_all(bind=engine)
            logger.info("Database tables created")
        else:
            logger.info("Database file already exists, skipping creation")
        db_initialized = True

# Call init_db only once
with app.app_context():
    init_db()

if __name__ == "__main__":
    logger.info("Starting Flask backend on port 5000...")
    app.run(host="0.0.0.0", port=5000, debug=True)
