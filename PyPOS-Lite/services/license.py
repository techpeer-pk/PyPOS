"""Machine-locked license activation (Ed25519 signature verification).

A license key is only valid for the specific PC it was issued for, so the
.exe can't be copied to another machine and reused. Keys are generated
offline by the vendor using vendor-tools/keygen.py (not shipped with the app).
"""
import base64
import hashlib
import platform
import subprocess
import winreg

from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey

from database import get_setting, set_setting

# Vendor's public key. Only the matching private key (kept offline by the
# vendor, never shipped) can produce a signature this verifies as valid.
VENDOR_PUBLIC_KEY_B64 = "uTpgPlc9o5PUfAIqtTQRoPW6fs+YueUjJtBHyVDgDgI="

_public_key = Ed25519PublicKey.from_public_bytes(base64.b64decode(VENDOR_PUBLIC_KEY_B64))


def _machine_guid():
    try:
        key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Cryptography")
        value, _ = winreg.QueryValueEx(key, "MachineGuid")
        return value
    except OSError:
        return ""


def _volume_serial():
    try:
        result = subprocess.run(
            ["cmd", "/c", "vol", "C:"],
            capture_output=True, text=True, timeout=5,
            creationflags=subprocess.CREATE_NO_WINDOW,
        )
        return result.stdout.strip()
    except Exception:
        return ""


def get_machine_id():
    """Stable ID derived from this PC's hardware, formatted for easy sharing."""
    raw = f"{_machine_guid()}|{_volume_serial()}|{platform.node()}"
    digest = hashlib.sha256(raw.encode("utf-8")).hexdigest().upper()[:16]
    return "-".join(digest[i:i + 4] for i in range(0, 16, 4))


def verify_key(machine_id, license_key):
    try:
        signature = base64.b64decode(license_key.strip())
        _public_key.verify(signature, machine_id.encode("utf-8"))
        return True
    except (InvalidSignature, ValueError):
        return False


def is_activated():
    stored_key = get_setting("license_key")
    if not stored_key:
        return False
    return verify_key(get_machine_id(), stored_key)


def activate(license_key):
    if verify_key(get_machine_id(), license_key):
        set_setting("license_key", license_key.strip())
        return True
    return False
