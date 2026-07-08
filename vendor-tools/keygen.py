"""
Vendor-only tool: generate a PyPOS-Lite license key for one customer PC.

This script is safe to keep in the repo -- it contains no secret. The
actual signing secret is private_key.pem, which lives OUTSIDE this repo
and must never be committed or shared. Anyone holding that file can
license any machine, so keep it backed up somewhere safe and private
(e.g. a password manager or printed QR backup) -- if it's lost, no new
keys can ever be issued.

The key's location is resolved in this order, so it works on any
laptop/account without editing this file:
  1. --key PATH command-line option
  2. PYPOS_VENDOR_KEY environment variable
  3. Default: C:\\Users\\TechPeer\\PyPOS-Vendor-Keys\\private_key.pem
     (only correct on this specific Windows account -- on a different
     laptop/username, use --key or the env var instead)

Usage:
    python keygen.py <MACHINE-ID>
    python keygen.py <MACHINE-ID> --key "D:\\some\\other\\private_key.pem"

The customer gets the Machine ID from the Activation screen in PyPOS-Lite
and sends it to you. Paste the resulting License Key back to them.
"""
import argparse
import base64
import os
import sys
from pathlib import Path

from cryptography.hazmat.primitives.serialization import load_pem_private_key

DEFAULT_PRIVATE_KEY_PATH = Path(r"C:\Users\TechPeer\PyPOS-Vendor-Keys\private_key.pem")


def resolve_key_path(cli_arg):
    if cli_arg:
        return Path(cli_arg)
    env_value = os.environ.get("PYPOS_VENDOR_KEY")
    if env_value:
        return Path(env_value)
    return DEFAULT_PRIVATE_KEY_PATH


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("machine_id")
    parser.add_argument("--key", dest="key_path", default=None,
                         help="Path to private_key.pem (overrides default/env var)")
    args = parser.parse_args()

    key_path = resolve_key_path(args.key_path)
    if not key_path.exists():
        print(f"Private key not found at {key_path}")
        print("On a different laptop/account? Use --key PATH or set PYPOS_VENDOR_KEY.")
        sys.exit(1)

    machine_id = args.machine_id.strip().upper()
    private_key = load_pem_private_key(key_path.read_bytes(), password=None)
    signature = private_key.sign(machine_id.encode("utf-8"))
    license_key = base64.b64encode(signature).decode("ascii")

    print(f"Machine ID:  {machine_id}")
    print(f"License Key: {license_key}")


if __name__ == "__main__":
    main()
