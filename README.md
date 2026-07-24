# PyPOS-Lite

A lightweight, offline point-of-sale desktop app for small stationary/retail shops, built with PyQt6 and SQLite. Ships as a single standalone `.exe` — no Python install, no internet connection required.

Built as a fixed-scope commercial project (see [PyPOS-LITE-35K-PLAN.md](PyPOS-LITE-35K-PLAN.md) for the original spec).

## Features

- **Dashboard** — today's sales total, invoice count, low-stock alerts
- **Sales / New Sale** — barcode scan or manual lookup, cart with live totals, thermal receipt printing (falls back to a saved `.txt` copy if the printer isn't reachable)
- **Inventory** — product list with SKU/price/stock, search, low-stock flags, add/edit products
- **Daily Sales Report** — invoice list with totals, average, and count; printable
- **Settings** — shop info, printer (COM port) and scanner config, database backup/restore, and a PIN-protected Danger Zone for clearing test data between clients
- **PIN lock** — Inventory and Settings are gated behind an admin PIN
- **Machine-locked activation** — the app won't run until activated with a license key tied to that PC's hardware ID (Ed25519-signed), preventing the `.exe` from being copied and reused elsewhere

## Project layout

```
PyPOS-Lite/
├── main.py              # App entry point / main window
├── config.py             # Paths, app constants
├── database.py           # SQLite connection + schema
├── models.py              # Product / Invoice data access
├── ui/                    # PyQt6 screens (dashboard, sales, inventory, reports, settings, PIN/lock, activation)
├── services/              # backup, license verification, printer (ESC/POS), scanner
├── assets/                 # icons/images
└── PyPOS-Lite.spec         # PyInstaller build spec

vendor-tools/               # Internal-only: license key generation for vendor use (not for client machines)
```

## Requirements

- Python 3.10+
- Windows (uses `winreg` for machine ID and COM ports for the printer)

## Setup

```bash
cd PyPOS-Lite
pip install -r requirements.txt
python main.py
```

On first run you'll be asked to activate with a license key tied to the machine's hardware ID. See [PyPOS-Lite/HELP-VENDOR.txt](PyPOS-Lite/HELP-VENDOR.txt) for the installer-facing setup/activation guide.

## Building the .exe

```bash
pip install pyinstaller
pyinstaller --onefile --windowed --name PyPOS-Lite --icon=assets\icon.ico --add-data "assets;assets" main.py
```

Output goes to `PyPOS-Lite/dist/PyPOS-Lite.exe`. See [vendor-tools/HELP-ME.txt](vendor-tools/HELP-ME.txt) for the full build/delivery/activation workflow (internal use only).

## License

Proprietary — All rights reserved. This is closed-source commercial software; see the activation system in `services/license.py` for the licensing mechanism used to control distribution.
