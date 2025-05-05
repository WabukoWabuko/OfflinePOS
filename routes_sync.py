import logging
import requests
import shutil
from flask import Blueprint, jsonify, send_file, request
from database import SessionLocal
from models import CachedSale
from sqlalchemy.orm import Session

sync_bp = Blueprint('sync', __name__)
logger = logging.getLogger(__name__)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def is_internet_available():
    try:
        requests.get("https://www.google.com", timeout=5)
        return True
    except requests.RequestException:
        return False

@sync_bp.route('/check-internet', methods=['GET'])
def check_internet():
    online = is_internet_available()
    logger.info(f"Internet check: {'Online' if online else 'Offline'}")
    print(f"Internet check: {'Online' if online else 'Offline'}")
    return jsonify({"online": online})

@sync_bp.route('/sync', methods=['POST'])
def sync():
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

@sync_bp.route('/backup', methods=['GET'])
def backup():
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

@sync_bp.route('/restore', methods=['POST'])
def restore():
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
