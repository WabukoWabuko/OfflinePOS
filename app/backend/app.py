import os
import sys
import logging
from flask import Flask, request, jsonify
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from app.db.database import SessionLocal, init_db
from app.db.models import User
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
    init_db()
    logger.info("Database initialized successfully")
except Exception as e:
    logger.error(f"Failed to initialize database: {e}")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.route('/api/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        logger.info(f"Login attempt for username: {username}")

        db = next(get_db())
        user = db.query(User).filter(User.username == username).first()

        if user and bcrypt.checkpw(password.encode('utf-8'), user.password_hash.encode('utf-8')):
            logger.info(f"Login successful for user: {username}")
            return jsonify({"message": "Login successful", "user_id": user.id, "role": user.role}), 200
        logger.warning(f"Invalid credentials for username: {username}")
        return jsonify({"message": "Invalid credentials"}), 401
    except Exception as e:
        logger.error(f"Login error: {e}")
        return jsonify({"message": "Server error"}), 500

@app.route('/api/register', methods=['POST'])
def register():
    try:
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        role = data.get('role', 'cashier')
        logger.info(f"Register attempt for username: {username}")

        db = next(get_db())
        if db.query(User).filter(User.username == username).first():
            logger.warning(f"Username already exists: {username}")
            return jsonify({"message": "Username already exists"}), 400

        password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        new_user = User(username=username, password_hash=password_hash, role=role)
        db.add(new_user)
        db.commit()
        logger.info(f"User registered: {username}")
        return jsonify({"message": "User registered successfully"}), 201
    except Exception as e:
        logger.error(f"Register error: {e}")
        return jsonify({"message": "Server error"}), 500

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
