"""USB barcode scanner support.

Standard USB barcode scanners act as a keyboard (HID keyboard-wedge):
they type the scanned code into whatever text field has focus, followed
by an Enter keypress. No special driver code is needed — the Sales
screen's barcode input field with an Enter-key handler already captures
scans. This module just normalizes the raw scanned text.
"""


def normalize_code(raw_code):
    """Strip whitespace/control characters some scanners prefix or suffix."""
    return raw_code.strip().strip("\r\n\t")
