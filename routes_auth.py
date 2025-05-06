import logging
from flask import Blueprint, request, jsonify, session
from database import SessionLocal
from models import User
from sqlalchemy.orm import Session
import bcrypt

auth_bp = Blueprint('auth', __name__, url_prefix='/api')
logger = logging.getLogger(__name__)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@auth_bp.route('/login', methods=['POST'])
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
            session['user_id'] = user.id
            session['role'] = user.role
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

@auth_bp.route('/register', methods=['POST'])
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

@auth_bp.route('/logout', methods=['POST'])
def logout():
    session.pop('user_id', None)
    session.pop('role', None)
    return jsonify({"message": "Logged out successfully"}), 200
