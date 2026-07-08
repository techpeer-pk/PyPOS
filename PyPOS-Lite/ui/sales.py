from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QLineEdit,
    QTableWidget, QTableWidgetItem, QComboBox, QMessageBox, QHeaderView,
    QDialog, QTextEdit, QDialogButtonBox, QCompleter
)
from PyQt6.QtCore import Qt, QStringListModel, QTimer
from PyQt6.QtGui import QFont

from models import Product, Invoice, StockError
from services.scanner import normalize_code
from services.printer import print_receipt, format_receipt_text
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
        self.scan_input.setPlaceholderText("Scan barcode, type SKU, or search by name...")
        self.scan_input.returnPressed.connect(self.scan_item)
        scan_btn = QPushButton("Scan")
        scan_btn.clicked.connect(self.scan_item)
        scan_row.addWidget(self.scan_input)
        scan_row.addWidget(scan_btn)
        layout.addLayout(scan_row)

        self._completer_map = {}
        self._completer_model = QStringListModel()
        self.completer = QCompleter()
        self.completer.setModel(self._completer_model)
        self.completer.setCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
        self.completer.setFilterMode(Qt.MatchFlag.MatchContains)
        self.completer.setCompletionMode(QCompleter.CompletionMode.UnfilteredPopupCompletion)
        self.completer.activated.connect(self.on_suggestion_selected)
        self.scan_input.setCompleter(self.completer)
        self.scan_input.textEdited.connect(self.update_suggestions)

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
        self.scan_input.clear()
        self._completer_map = {}
        self._completer_model.setStringList([])
        self.scan_input.setFocus()

    def update_suggestions(self, text):
        text = text.strip()
        if not text:
            self._completer_map = {}
            self._completer_model.setStringList([])
            return
        matches = Product.search(text)[:10]
        self._completer_map = {
            f"{p['name']} ({p['sku']}) - Rs.{p['price']:.0f}": p["sku"] for p in matches
        }
        self._completer_model.setStringList(list(self._completer_map.keys()))

    def on_suggestion_selected(self, display_text):
        sku = self._completer_map.pop(display_text, None)
        # Qt re-fills the line edit with the completion text right after this
        # slot runs, so defer the clear until that settles.
        QTimer.singleShot(0, self.scan_input.clear)
        if not sku:
            return
        product = Product.get_by_sku(sku)
        if product:
            self._add_product_to_cart(product)

    def scan_item(self):
        raw_text = self.scan_input.text()
        if raw_text in self._completer_map:
            self.on_suggestion_selected(raw_text)
            return

        text = normalize_code(raw_text)
        self.scan_input.clear()
        if not text:
            return
        product = Product.get_by_sku(text)
        if not product:
            matches = Product.search(text)
            if len(matches) == 1:
                product = matches[0]
            elif len(matches) > 1:
                QMessageBox.information(
                    self, "Multiple Matches",
                    "Multiple products match. Please pick one from the dropdown list.",
                )
                return
        if not product:
            QMessageBox.warning(self, "Not Found", "Product not found. Add first.")
            return
        self._add_product_to_cart(product)

    def _add_product_to_cart(self, product):
        for item in self.cart:
            if item["sku"] == product["sku"]:
                item["qty"] += 1
                self.render_cart()
                return
        self.cart.append({
            "sku": product["sku"],
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

        status = (
            f"Printer not responding. Check cable.\nReceipt saved to:\n{fallback_path}"
            if fallback_path else "Receipt printed."
        )
        self.show_receipt_preview(shop_name, invoice, status)

        self.cart = []
        self.render_cart()
        self.scan_input.setFocus()

    def show_receipt_preview(self, shop_name, invoice, status_line):
        dialog = QDialog(self)
        dialog.setWindowTitle(f"Invoice {invoice['id']}")

        layout = QVBoxLayout(dialog)
        text = QTextEdit()
        text.setReadOnly(True)
        text.setFont(QFont("Courier New", 10))
        text.setPlainText(format_receipt_text(shop_name, invoice))
        layout.addWidget(text)

        status_label = QLabel(status_line)
        layout.addWidget(status_label)

        buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok)
        buttons.accepted.connect(dialog.accept)
        layout.addWidget(buttons)

        dialog.resize(380, 500)
        dialog.exec()
