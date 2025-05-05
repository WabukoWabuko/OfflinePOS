import os
import logging
import requests
import shutil
from flask import Flask, request, jsonify, send_file
from database import SessionLocal, init_db, cache_sale
from models import User, CachedSale
from sqlalchemy.orm import Session
import bcrypt

# Set up logging
os.makedirs('logs', exist_ok=True)
logging.basicConfig(
    filename='logs/backend.log',
    level=logging.INFO,
    format='%(asctime)s %(levelname)s: %(message)s'
)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Initialize the database
try:
    print("Attempting to initialize database...")
    init_db()
    logger.info("Database initialized successfully")
    print("Database initialized successfully")
except Exception as e:
    logger.error(f"Failed to initialize database: {str(e)}")
    print(f"Failed to initialize database: {str(e)}")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def is_internet_available():
    """Check if internet is available."""
    try:
        requests.get("https://www.google.com", timeout=5)
        return True
    except requests.RequestException:
        return False

@app.route('/api/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        logger.info(f"Login attempt for username: {username}")
        print(f"Login attempt for username: {username}")

        db = next(get_db())
        user = db.query(User).filter(User.username == username).first()

        if user and bcrypt.checkpw(password.encode('utf-8'), user.password_hash.encode('utf-8')):
            logger.info(f"Login successful for user: {username}")
            print(f"Login successful for user: {username}")
            return jsonify({"message": "Login successful", "user_id": user.id, "role": user.role}), 200
        logger.warning(f"Invalid credentials for username: {username}")
        print(f"Invalid credentials for username: {username}")
        return jsonify({"message": "Invalid credentials"}), 401
    except Exception as e:
        logger.error(f"Login error: {str(e)}")
        print(f"Login error: {str(e)}")
        return jsonify({"message": "Server error"}), 500

@app.route('/api/register', methods=['POST'])
def register():
    try:
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        role = data.get('role', 'cashier')
        logger.info(f"Register attempt for username: {username}")
        print(f"Register attempt for username: {username}")

        db = next(get_db())
        if db.query(User).filter(User.username == username).first():
            logger.warning(f"Username already exists: {username}")
            print(f"Username already exists: {username}")
            return jsonify({"message": "Username already exists"}), 400

        password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        new_user = User(username=username, password_hash=password_hash, role=role)
        db.add(new_user)
        db.commit()
        logger.info(f"User registered: {username}")
        print(f"User registered: {username}")
        return jsonify({"message": "User registered successfully"}), 201
    except Exception as e:
        logger.error(f"Register error: {str(e)}")
        print(f"Register error: {str(e)}")
        return jsonify({"message": "Server error"}), 500

@app.route('/api/check-internet', methods=['GET'])
def check_internet():
    """Check internet connectivity."""
    online = is_internet_available()
    logger.info(f"Internet check: {'Online' if online else 'Offline'}")
    print(f"Internet check: {'Online' if online else 'Offline'}")
    return jsonify({"online": online})

@app.route('/api/sync', methods=['POST'])
def sync():
    """Placeholder for cloud synchronization."""
    if not is_internet_available():
        return jsonify({"message": "Offline; sync unavailable"}), 503
    try:
        db = next(get_db())
        pending_sales = db.query(CachedSale).filter(CachedSale.synced == 0).all()
        logger.info(f"Found {len(pending_sales)} pending sales to sync")
        print(f"Found {len(pending_sales)} pending sales to sync")
        # Placeholder: Simulate sync (replace with real API call)
        for sale in pending_sales:
            sale.synced = 1
        db.commit()
        logger.info("Sync completed")
        print("Sync completed")
        return jsonify({"message": "Sync successful", "synced": len(pending_sales)}), 200
    except Exception as e:
        logger.error(f"Sync error: {str(e)}")
        print(f"Sync error: {str(e)}")
        return jsonify({"message": "Server error"}), 500

@app.route('/api/backup', methods=['GET'])
def backup():
    """Create a backup of the database."""
    try:
        backup_path = '/app/offline_pos_backup.db'
        shutil.copyfile('/app/offline_pos.db', backup_path)
        logger.info(f"Backup created at {backup_path}")
        print(f"Backup created at {backup_path}")
        return send_file(backup_path, as_attachment=True, download_name='offline_pos_backup.db')
    except Exception as e:
        logger.error(f"Backup error: {str(e)}")
        print(f"Backup error: {str(e)}")
        return jsonify({"message": "Server error"}), 500

@app.route('/api/restore', methods=['POST'])
def restore():
    """Restore the database from a backup."""
    if 'file' not in request.files:
        return jsonify({"message": "No file provided"}), 400
    backup_file = request.files['file']
    try:
        backup_path = '/app/offline_pos_backup.db'
        backup_file.save(backup_path)
        shutil.copyfile(backup_path, '/app/offline_pos.db')
        logger.info("Database restored from backup")
        print("Database restored from backup")
        return jsonify({"message": "Restore successful"}), 200
    except Exception as e:
        logger.error(f"Restore error: {str(e)}")
        print(f"Restore error: {str(e)}")
        return jsonify({"message": "Server error"}), 500

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
