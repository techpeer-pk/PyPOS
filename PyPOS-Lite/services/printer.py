"""Thermal receipt printer (ESC/POS) over a serial/USB COM port.

Falls back to saving a plain-text copy of the receipt when the printer
is not reachable, per the plan's error-handling rules.
"""
import os

import serial

from config import BASE_DIR

ESC = b"\x1b"
GS = b"\x1d"
INIT = ESC + b"@"
CUT = GS + b"V\x01"

RECEIPT_WIDTH = 40


class PrinterError(Exception):
    pass


DEVELOPER_FOOTER = "Developed By: TechPeer +92 309 0404 293"


def format_receipt_text(shop_name, invoice, phone=""):
    lines = [
        "=" * RECEIPT_WIDTH,
        (shop_name or "STATIONARY SHOP").center(RECEIPT_WIDTH),
        "Receipt".center(RECEIPT_WIDTH),
        "=" * RECEIPT_WIDTH,
    ]
    if phone:
        lines.append(f"Phone: {phone}".center(RECEIPT_WIDTH))
    lines += [
        f"Date: {invoice['date']}",
        f"Invoice: {invoice['id']}",
        "",
    ]
    for item in invoice["items"]:
        name = item["name"][:18].ljust(18)
        qty = f"{item['quantity']}x"
        unit_price = item["unit_price"]
        line_total = item["quantity"] * unit_price
        lines.append(f"{name} {qty:>4} {unit_price:>6.0f} = {line_total:>7.0f}")
    lines += [
        "-" * RECEIPT_WIDTH,
        f"TOTAL:{invoice['total']:>{RECEIPT_WIDTH - 6}.0f} PKR",
        f"Payment: {invoice['payment_method']}",
        "Status: PAID",
        "",
        "Thank you! Come again.".center(RECEIPT_WIDTH),
        "=" * RECEIPT_WIDTH,
        DEVELOPER_FOOTER.center(RECEIPT_WIDTH),
    ]
    return "\n".join(lines) + "\n"


def format_report_text(shop_name, date_str, invoices):
    lines = [
        "=" * RECEIPT_WIDTH,
        (shop_name or "STATIONARY SHOP").center(RECEIPT_WIDTH),
        f"Daily Sales Report - {date_str}".center(RECEIPT_WIDTH),
        "=" * RECEIPT_WIDTH,
    ]
    total = 0
    for inv in invoices:
        time_part = inv["date"].split(" ")[1] if " " in inv["date"] else ""
        lines.append(f"{inv['id']} {time_part} x{inv['items_count']:<3} {inv['total']:>8.0f}")
        total += inv["total"]
    count = len(invoices)
    avg = (total / count) if count else 0
    lines += [
        "-" * RECEIPT_WIDTH,
        f"Total Sales: {total:.0f} PKR",
        f"Invoices: {count}   Avg: {avg:.0f} PKR",
        "=" * RECEIPT_WIDTH,
    ]
    return "\n".join(lines) + "\n"


def _write_to_port(port, text, baudrate=9600, timeout=2):
    data = INIT + text.encode("ascii", "replace") + b"\n\n\n" + CUT
    with serial.Serial(port, baudrate=baudrate, timeout=timeout) as conn:
        conn.write(data)


def _save_to_file(name, text):
    receipts_dir = os.path.join(BASE_DIR, "receipts")
    os.makedirs(receipts_dir, exist_ok=True)
    path = os.path.join(receipts_dir, f"{name}.txt")
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)
    return path


def print_receipt(shop_name, invoice, port, phone=""):
    """Returns None on successful print, or a file path if it fell back to saving."""
    text = format_receipt_text(shop_name, invoice, phone)
    try:
        _write_to_port(port, text)
        return None
    except Exception:
        return _save_to_file(invoice["id"], text)


def print_report(shop_name, date_str, invoices, port):
    text = format_report_text(shop_name, date_str, invoices)
    try:
        _write_to_port(port, text)
        return None
    except Exception:
        return _save_to_file(f"report_{date_str}", text)


def test_print(port):
    try:
        _write_to_port(port, "PyPOS-Lite Test Print\nPrinter is working!\n")
    except Exception as e:
        raise PrinterError(str(e)) from e
