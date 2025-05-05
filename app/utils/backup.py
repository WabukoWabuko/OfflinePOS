import shutil
import os
from datetime import datetime

def backup_database(db_path="offline_pos.db", backup_dir="backups"):
    """Create a backup of the SQLite database."""
    if not os.path.exists(backup_dir):
        os.makedirs(backup_dir)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = os.path.join(backup_dir, f"offline_pos_{timestamp}.db")
    shutil.copy2(db_path, backup_path)
    return {"status": "success", "message": f"Backup created at {backup_path}"}

def restore_database(backup_path, db_path="offline_pos.db"):
    """Restore the SQLite database from a backup."""
    if not os.path.exists(backup_path):
        return {"status": "error", "message": f"Backup {backup_path} not found"}
    shutil.copy2(backup_path, db_path)
    return {"status": "success", "message": f"Restored from {backup_path}"}

if __name__ == "__main__":
    # Test backup
    print(backup_database())
    # Test restore (replace with actual backup file path)
    # print(restore_database("backups/offline_pos_20250503_123456.db"))
