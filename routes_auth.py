import logging
from flask import Blueprint, request, jsonify, session
from database import SessionLocal
from models import User
from sqlalchemy.orm import Session
from bcrypt import hashpw, gensalt, checkpw

auth_bp = Blueprint('auth', __name__, url_prefix='/api')
logger = logging.getLogger(__name__)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def hash_password(password: str) -> str:
    salt = gensalt()
    hashed = hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')

@auth_bp.route('/check-session', methods=['GET'])
def check_session():
    try:
        user_id = session.get('user_id')
        if user_id:
            db = next(get_db())
            user = db.query(User).filter(User.id == user_id).first()
            if user:
                return jsonify({"user_id": user.id, "role": user.role}), 200
        return jsonify({"message": "No active session"}), 401
    except Exception as e:
        logger.error(f"Check session error: {str(e)}")
        return jsonify({"message": "Server error"}), 500

@auth_bp.route('/register', methods=['POST'])
def register():
    try:
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        role = data.get('role', 'user')

        if not username or not password:
            logger.warning("Registration failed: Missing username or password")
            return jsonify({"message": "Username and password are required"}), 400

        db = next(get_db())
        if db.query(User).filter(User.username == username).first():
            logger.warning(f"Registration failed: Username {username} already exists")
            return jsonify({"message": "Username already exists"}), 400

        hashed_password = hash_password(password)
        user = User(username=username, password_hash=hashed_password, role=role)
        db.add(user)
        db.commit()
        logger.info(f"User registered: {username}, ID: {user.id}")
        return jsonify({"message": "User registered successfully", "user_id": user.id}), 201
    except Exception as e:
        logger.error(f"Register error: {str(e)}")
        return jsonify({"message": f"Server error: {str(e)}"}), 500

@auth_bp.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')

        if not username or not password:
            logger.warning("Login failed: Missing username or password")
            return jsonify({"message": "Username and password are required"}), 400

        db = next(get_db())
        user = db.query(User).filter(User.username == username).first()
        if not user:
            logger.warning(f"Login failed: Username {username} not found")
            return jsonify({"message": "Invalid credentials"}), 401

        if user.password_hash is None:
            logger.error("Login failed: Password hash is None")
            return jsonify({"message": "Server error: Password hash missing"}), 500

        if not checkpw(password.encode('utf-8'), user.password_hash.encode('utf-8')):
            logger.warning(f"Login failed: Invalid password for {username}")
            return jsonify({"message": "Invalid credentials"}), 401

        session['user_id'] = user.id
        logger.info(f"User logged in: {username}, ID: {user.id}")
        return jsonify({"message": "Login successful", "user_id": user.id, "role": user.role}), 200
    except Exception as e:
        logger.error(f"Login error: {str(e)}")
        return jsonify({"message": f"Server error: {str(e)}"}), 500

@auth_bp.route('/logout', methods=['POST'])
def logout():
    try:
        session.pop('user_id', None)
        logger.info("User logged out")
        return jsonify({"message": "Logout successful"}), 200
    except Exception as e:
        logger.error(f"Logout error: {str(e)}")
        return jsonify({"message": f"Server error: {str(e)}"}), 500
