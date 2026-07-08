"""App-wide constants for PyPOS-Lite."""
import os
import sys

if getattr(sys, "frozen", False):
    BASE_DIR = os.path.dirname(sys.executable)
    ASSETS_DIR = os.path.join(getattr(sys, "_MEIPASS", BASE_DIR), "assets")
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    ASSETS_DIR = os.path.join(BASE_DIR, "assets")

DB_PATH = os.path.join(BASE_DIR, "data.db")
BACKUP_DIR = os.path.join(BASE_DIR, "backups")
ICON_PATH = os.path.join(ASSETS_DIR, "icon.png")

DEFAULT_REORDER_LEVEL = 5
APP_NAME = "PyPOS-Lite"
