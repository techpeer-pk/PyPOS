from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QLineEdit,
    QTableWidget, QTableWidgetItem, QMessageBox, QDialog, QFormLayout,
    QDialogButtonBox, QHeaderView
)
from PyQt6.QtCore import Qt

from models import Product


class ProductDialog(QDialog):
    def __init__(self, parent=None, product=None):
        super().__init__(parent)
        self.product = product
        self.setWindowTitle("Edit Product" if product else "Add New Product")

        layout = QFormLayout(self)
        self.name_input = QLineEdit(product["name"] if product else "")
        self.sku_input = QLineEdit(product["sku"] if product else "")
        self.price_input = QLineEdit(str(product["price"]) if product else "")
        self.stock_input = QLineEdit(str(product["stock"]) if product else "0")
        self.reorder_input = QLineEdit(str(product["reorder_level"]) if product else "5")

        self.sku_manually_edited = False
        if product:
            self.sku_input.setEnabled(False)
        else:
            self.sku_input.setPlaceholderText("Auto-generated (or scan/type real barcode)")
            self.sku_input.textEdited.connect(self._mark_sku_manual)
            self.name_input.textChanged.connect(self._autofill_sku)

        layout.addRow("Name:", self.name_input)
        layout.addRow("SKU:", self.sku_input)
        layout.addRow("Price:", self.price_input)
        layout.addRow("Stock:", self.stock_input)
        layout.addRow("Reorder Level:", self.reorder_input)

        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )
        buttons.accepted.connect(self.validate_and_accept)
        buttons.rejected.connect(self.reject)
        layout.addRow(buttons)

    def _mark_sku_manual(self):
        self.sku_manually_edited = True

    def _autofill_sku(self, name):
        if self.sku_manually_edited:
            return
        name = name.strip()
        if not name:
            self.sku_input.clear()
            return
        self.sku_input.setText(Product.generate_sku(name))

    def validate_and_accept(self):
        if not self.name_input.text().strip() or not self.sku_input.text().strip():
            QMessageBox.warning(self, "Missing Info", "Name and SKU are required.")
            return
        try:
            float(self.price_input.text())
            int(self.stock_input.text())
            int(self.reorder_input.text())
        except ValueError:
            QMessageBox.warning(self, "Invalid Input", "Price/Stock/Reorder must be numbers.")
            return
        self.accept()

    def get_data(self):
        return {
            "name": self.name_input.text().strip(),
            "sku": self.sku_input.text().strip(),
            "price": float(self.price_input.text()),
            "stock": int(self.stock_input.text()),
            "reorder_level": int(self.reorder_input.text()),
        }


class InventoryScreen(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window

        layout = QVBoxLayout(self)

        title = QLabel("INVENTORY MANAGEMENT")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("font-size: 20px; font-weight: bold; padding: 10px;")
        layout.addWidget(title)

        top_row = QHBoxLayout()
        add_btn = QPushButton("+ Add New")
        back_btn = QPushButton("Back")
        add_btn.clicked.connect(self.add_product)
        back_btn.clicked.connect(main_window.show_dashboard)
        top_row.addWidget(add_btn)
        top_row.addStretch()
        top_row.addWidget(back_btn)
        layout.addLayout(top_row)

        search_row = QHBoxLayout()
        search_row.addWidget(QLabel("Search:"))
        self.search_input = QLineEdit()
        self.search_input.textChanged.connect(self.render_table)
        search_row.addWidget(self.search_input)
        layout.addLayout(search_row)

        self.table = QTableWidget(0, 5)
        self.table.setHorizontalHeaderLabels(["Product", "SKU", "Price", "Stock", "Action"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        layout.addWidget(self.table)

        self.summary_label = QLabel()
        layout.addWidget(self.summary_label)

    def refresh(self):
        self.search_input.clear()
        self.render_table()

    def render_table(self):
        term = self.search_input.text().strip()
        products = Product.search(term) if term else Product.get_all()

        self.table.setRowCount(len(products))
        for row, p in enumerate(products):
            self.table.setItem(row, 0, QTableWidgetItem(p["name"]))
            self.table.setItem(row, 1, QTableWidgetItem(p["sku"]))
            self.table.setItem(row, 2, QTableWidgetItem(f"{p['price']:.0f}"))
            stock_text = str(p["stock"])
            if p["stock"] <= p["reorder_level"]:
                stock_text += " ⚠"
            self.table.setItem(row, 3, QTableWidgetItem(stock_text))

            edit_btn = QPushButton("Edit")
            edit_btn.clicked.connect(lambda checked, sku=p["sku"]: self.edit_product(sku))
            self.table.setCellWidget(row, 4, edit_btn)

        all_products = Product.get_all()
        low_count = len(Product.low_stock())
        self.summary_label.setText(
            f"Total Products: {len(all_products)}   Low Stock Items: {low_count}"
        )

    def add_product(self):
        dialog = ProductDialog(self)
        if dialog.exec():
            data = dialog.get_data()
            if Product.get_by_sku(data["sku"]):
                QMessageBox.warning(self, "Duplicate SKU", "A product with this SKU already exists.")
                return
            Product.add(data["name"], data["sku"], data["price"], data["stock"], data["reorder_level"])
            self.render_table()

    def edit_product(self, sku):
        product = Product.get_by_sku(sku)
        if not product:
            return
        dialog = ProductDialog(self, product)
        if dialog.exec():
            data = dialog.get_data()
            Product.update(sku, name=data["name"], price=data["price"], reorder_level=data["reorder_level"])
            Product.update_stock(sku, data["stock"])
            self.render_table()
