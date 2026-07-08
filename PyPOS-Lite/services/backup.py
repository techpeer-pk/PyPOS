"""Simple backup/restore for data.db."""
import os
import shutil
from datetime import datetime

from config import DB_PATH, BACKUP_DIR


def backup_now():
    os.makedirs(BACKUP_DIR, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    dest = os.path.join(BACKUP_DIR, f"data_backup_{timestamp}.db")
    shutil.copy2(DB_PATH, dest)
    return dest


def restore(backup_path):
    shutil.copy2(backup_path, DB_PATH)


def list_backups():
    if not os.path.isdir(BACKUP_DIR):
        return []
    files = [f for f in os.listdir(BACKUP_DIR) if f.endswith(".db")]
    files.sort(reverse=True)
    return files


def get_last_backup_time():
    backups = list_backups()
    if not backups:
        return None
    path = os.path.join(BACKUP_DIR, backups[0])
    return datetime.fromtimestamp(os.path.getmtime(path))
