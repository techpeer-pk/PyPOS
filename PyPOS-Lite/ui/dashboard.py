from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QGroupBox, QListWidget
)
from PyQt6.QtCore import Qt

from models import Product, Invoice


class DashboardScreen(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window

        layout = QVBoxLayout(self)

        header_row = QHBoxLayout()
        title = QLabel("PyPOS-LITE DASHBOARD")
        title.setStyleSheet("font-size: 20px; font-weight: bold; padding: 10px;")
        lock_btn = QPushButton("🔒")
        lock_btn.setFixedWidth(36)
        lock_btn.setToolTip("Lock POS")
        lock_btn.clicked.connect(main_window.show_lock_screen)
        settings_btn = QPushButton("⚙")
        settings_btn.setFixedWidth(36)
        settings_btn.setToolTip("Settings")
        settings_btn.clicked.connect(main_window.show_settings)
        header_row.addWidget(title)
        header_row.addStretch()
        header_row.addWidget(lock_btn)
        header_row.addWidget(settings_btn)
        layout.addLayout(header_row)

        top_bar = QHBoxLayout()
        new_sale_btn = QPushButton("NEW SALE")
        products_btn = QPushButton("PRODUCTS")
        reports_btn = QPushButton("REPORTS")
        exit_btn = QPushButton("EXIT")

        new_sale_btn.clicked.connect(main_window.show_sales)
        products_btn.clicked.connect(main_window.show_inventory)
        reports_btn.clicked.connect(main_window.show_reports)
        exit_btn.clicked.connect(main_window.close)

        for btn in (new_sale_btn, products_btn, reports_btn, exit_btn):
            btn.setMinimumHeight(40)
            top_bar.addWidget(btn)
        layout.addLayout(top_bar)

        summary_box = QGroupBox("TODAY'S SALES SUMMARY")
        summary_layout = QVBoxLayout(summary_box)
        self.total_label = QLabel()
        self.count_label = QLabel()
        self.last_sale_label = QLabel()
        for lbl in (self.total_label, self.count_label, self.last_sale_label):
            lbl.setStyleSheet("font-size: 14px; padding: 2px;")
            summary_layout.addWidget(lbl)
        layout.addWidget(summary_box)

        low_stock_box = QGroupBox("LOW STOCK ALERTS")
        low_stock_layout = QVBoxLayout(low_stock_box)
        self.low_stock_list = QListWidget()
        low_stock_layout.addWidget(self.low_stock_list)
        layout.addWidget(low_stock_box)

        quick_box = QGroupBox("QUICK ACTIONS")
        quick_layout = QHBoxLayout(quick_box)
        view_inventory_btn = QPushButton("View Inventory")
        view_reports_btn = QPushButton("View Reports")
        view_inventory_btn.clicked.connect(main_window.show_inventory)
        view_reports_btn.clicked.connect(main_window.show_reports)
        quick_layout.addWidget(view_inventory_btn)
        quick_layout.addWidget(view_reports_btn)
        layout.addWidget(quick_box)

        layout.addStretch()

    def refresh(self):
        today = Invoice.get_today_total()
        self.total_label.setText(f"Total Sales:   {today['total']:.0f} PKR")
        self.count_label.setText(f"Invoices:      {today['count']}")

        recent = Invoice.get_recent(1)
        if recent and " " in recent[0]["date"]:
            last_time = recent[0]["date"].split(" ")[1]
            self.last_sale_label.setText(f"Last Sale:     {last_time}")
        else:
            self.last_sale_label.setText("Last Sale:     -")

        self.low_stock_list.clear()
        low_items = Product.low_stock()
        if not low_items:
            self.low_stock_list.addItem("No low stock items")
        for item in low_items:
            self.low_stock_list.addItem(f"⚠ {item['name']} - Only {item['stock']} left")
