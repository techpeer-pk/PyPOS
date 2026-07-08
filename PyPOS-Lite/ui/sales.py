from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QLineEdit,
    QTableWidget, QTableWidgetItem, QComboBox, QMessageBox, QHeaderView
)
from PyQt6.QtCore import Qt

from models import Product, Invoice, StockError
from services.scanner import normalize_code
from services.printer import print_receipt
from ui.settings import get_setting


class SalesScreen(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.cart = []  # list of {sku, name, qty, unit_price}

        layout = QVBoxLayout(self)

        title = QLabel("NEW SALE - INVOICE")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("font-size: 20px; font-weight: bold; padding: 10px;")
        layout.addWidget(title)

        scan_row = QHBoxLayout()
        scan_row.addWidget(QLabel("Barcode/SKU:"))
        self.scan_input = QLineEdit()
        self.scan_input.returnPressed.connect(self.scan_item)
        scan_btn = QPushButton("Scan")
        scan_btn.clicked.connect(self.scan_item)
        scan_row.addWidget(self.scan_input)
        scan_row.addWidget(scan_btn)
        layout.addLayout(scan_row)

        self.table = QTableWidget(0, 4)
        self.table.setHorizontalHeaderLabels(["Item", "Qty", "Price Per", "Total"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.itemChanged.connect(self.on_item_changed)
        layout.addWidget(self.table)

        self.subtotal_label = QLabel("Subtotal: 0 PKR")
        self.total_label = QLabel("TOTAL: 0 PKR")
        self.total_label.setStyleSheet("font-size: 16px; font-weight: bold;")
        layout.addWidget(self.subtotal_label)
        layout.addWidget(self.total_label)

        payment_row = QHBoxLayout()
        payment_row.addWidget(QLabel("Payment:"))
        self.payment_combo = QComboBox()
        self.payment_combo.addItems(["Cash", "Card"])
        payment_row.addWidget(self.payment_combo)
        payment_row.addStretch()
        layout.addLayout(payment_row)

        action_row = QHBoxLayout()
        remove_btn = QPushButton("- Remove")
        clear_btn = QPushButton("Clear")
        complete_btn = QPushButton("COMPLETE & PRINT")
        back_btn = QPushButton("Back")
        remove_btn.clicked.connect(self.remove_selected)
        clear_btn.clicked.connect(self.clear_cart)
        complete_btn.clicked.connect(self.complete_sale)
        back_btn.clicked.connect(main_window.show_dashboard)
        action_row.addWidget(remove_btn)
        action_row.addWidget(clear_btn)
        action_row.addWidget(complete_btn)
        action_row.addWidget(back_btn)
        layout.addLayout(action_row)

        self.invoice_label = QLabel("Invoice #: -")
        layout.addWidget(self.invoice_label)

    def refresh(self):
        self.cart = []
        self.render_cart()
        self.invoice_label.setText("Invoice #: -")
        self.scan_input.setFocus()

    def scan_item(self):
        sku = normalize_code(self.scan_input.text())
        self.scan_input.clear()
        if not sku:
            return
        product = Product.get_by_sku(sku)
        if not product:
            QMessageBox.warning(self, "Not Found", "Product not found. Add first.")
            return
        for item in self.cart:
            if item["sku"] == sku:
                item["qty"] += 1
                self.render_cart()
                return
        self.cart.append({
            "sku": sku,
            "name": product["name"],
            "qty": 1,
            "unit_price": product["price"],
        })
        self.render_cart()

    def render_cart(self):
        self.table.blockSignals(True)
        self.table.setRowCount(len(self.cart))
        subtotal = 0
        for row, item in enumerate(self.cart):
            line_total = item["qty"] * item["unit_price"]
            subtotal += line_total

            name_item = QTableWidgetItem(item["name"])
            name_item.setFlags(name_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
            self.table.setItem(row, 0, name_item)

            qty_item = QTableWidgetItem(str(item["qty"]))
            self.table.setItem(row, 1, qty_item)

            price_item = QTableWidgetItem(f"{item['unit_price']:.0f}")
            price_item.setFlags(price_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
            self.table.setItem(row, 2, price_item)

            total_item = QTableWidgetItem(f"{line_total:.0f}")
            total_item.setFlags(total_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
            self.table.setItem(row, 3, total_item)

        self.table.blockSignals(False)
        self.subtotal_label.setText(f"Subtotal: {subtotal:.0f} PKR")
        self.total_label.setText(f"TOTAL: {subtotal:.0f} PKR")

    def on_item_changed(self, item):
        if item.column() != 1:
            return
        row = item.row()
        try:
            new_qty = int(item.text())
            if new_qty <= 0:
                raise ValueError
        except ValueError:
            QMessageBox.warning(self, "Invalid Qty", "Quantity must be a positive whole number.")
            self.render_cart()
            return
        self.cart[row]["qty"] = new_qty
        self.render_cart()

    def remove_selected(self):
        row = self.table.currentRow()
        if row < 0:
            return
        del self.cart[row]
        self.render_cart()

    def clear_cart(self):
        self.cart = []
        self.render_cart()

    def complete_sale(self):
        if not self.cart:
            QMessageBox.warning(self, "Empty Cart", "Add at least one item first.")
            return
        payment_method = self.payment_combo.currentText()
        items = [{"sku": i["sku"], "quantity": i["qty"]} for i in self.cart]
        try:
            invoice = Invoice.create(items, payment_method)
        except StockError as e:
            QMessageBox.warning(self, "Not enough stock!", str(e))
            return
        except ValueError as e:
            QMessageBox.warning(self, "Error", str(e))
            return

        self.invoice_label.setText(f"Invoice #: {invoice['id']}")

        shop_name = get_setting("shop_name")
        port = get_setting("printer_port", "COM4")
        fallback_path = print_receipt(shop_name, invoice, port)

        if fallback_path:
            QMessageBox.information(
                self, "Sale Complete",
                f"Invoice {invoice['id']} completed.\nTotal: {invoice['total']:.0f} PKR\n\n"
                f"Printer not responding. Check cable.\nReceipt saved to:\n{fallback_path}",
            )
        else:
            QMessageBox.information(
                self, "Sale Complete",
                f"Invoice {invoice['id']} completed.\nTotal: {invoice['total']:.0f} PKR\nReceipt printed.",
            )

        self.cart = []
        self.render_cart()
        self.scan_input.setFocus()
