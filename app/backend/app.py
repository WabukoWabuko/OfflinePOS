import os
import sys
# Add project root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from flask import Flask, request, jsonify
from app.db.database import SessionLocal, init_db
from app.db.models import User
from sqlalchemy.orm import Session
import bcrypt

app = Flask(__name__)

# Initialize the database
init_db()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    db = next(get_db())
    user = db.query(User).filter(User.username == username).first()

    if user and bcrypt.checkpw(password.encode('utf-8'), user.password_hash.encode('utf-8')):
        return jsonify({"message": "Login successful", "user_id": user.id, "role": user.role}), 200
    return jsonify({"message": "Invalid credentials"}), 401

@app.route('/api/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    role = data.get('role', 'cashier')

    db = next(get_db())
    if db.query(User).filter(User.username == username).first():
        return jsonify({"message": "Username already exists"}), 400

    password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    new_user = User(username=username, password_hash=password_hash, role=role)
    db.add(new_user)
    db.commit()

    return jsonify({"message": "User registered successfully"}), 201

if __name__ == "__main__":
    app.run(debug=True, port=5000)
