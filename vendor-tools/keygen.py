"""
Vendor-only tool: generate a PyPOS-Lite license key for one customer PC.

This script is safe to keep in the repo -- it contains no secret. The
actual signing secret is private_key.pem, which lives OUTSIDE this repo
(default: C:\\Users\\TechPeer\\PyPOS-Vendor-Keys\\private_key.pem) and must
never be committed or shared. Anyone holding that file can license any
machine, so keep it backed up somewhere safe and private (e.g. a password
manager or encrypted USB) -- if it's lost, no new keys can ever be issued.

Usage:
    python keygen.py <MACHINE-ID>

The customer gets the Machine ID from the Activation screen in PyPOS-Lite
and sends it to you. Paste the resulting License Key back to them.
"""
import base64
import sys
from pathlib import Path

from cryptography.hazmat.primitives.serialization import load_pem_private_key

DEFAULT_PRIVATE_KEY_PATH = Path(r"C:\Users\TechPeer\PyPOS-Vendor-Keys\private_key.pem")


def main():
    if len(sys.argv) != 2:
        print("Usage: python keygen.py <MACHINE-ID>")
        sys.exit(1)

    if not DEFAULT_PRIVATE_KEY_PATH.exists():
        print(f"Private key not found at {DEFAULT_PRIVATE_KEY_PATH}")
        sys.exit(1)

    machine_id = sys.argv[1].strip().upper()
    private_key = load_pem_private_key(DEFAULT_PRIVATE_KEY_PATH.read_bytes(), password=None)
    signature = private_key.sign(machine_id.encode("utf-8"))
    license_key = base64.b64encode(signature).decode("ascii")

    print(f"Machine ID:  {machine_id}")
    print(f"License Key: {license_key}")


if __name__ == "__main__":
    main()
