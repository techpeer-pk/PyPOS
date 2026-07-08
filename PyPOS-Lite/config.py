"""App-wide constants for PyPOS-Lite."""
import os
import sys

if getattr(sys, "frozen", False):
    BASE_DIR = os.path.dirname(sys.executable)
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DB_PATH = os.path.join(BASE_DIR, "data.db")
BACKUP_DIR = os.path.join(BASE_DIR, "backups")

DEFAULT_REORDER_LEVEL = 5
APP_NAME = "PyPOS-Lite"
