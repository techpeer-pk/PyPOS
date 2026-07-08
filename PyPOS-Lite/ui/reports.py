from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QTableWidget, QTableWidgetItem, QDateEdit, QMessageBox, QHeaderView
)
from PyQt6.QtCore import Qt, QDate

from models import Invoice
from services.printer import print_report as send_report_to_printer
from ui.settings import get_setting


class ReportsScreen(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window

        layout = QVBoxLayout(self)

        title = QLabel("DAILY SALES REPORT")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("font-size: 20px; font-weight: bold; padding: 10px;")
        layout.addWidget(title)

        date_row = QHBoxLayout()
        date_row.addWidget(QLabel("Date:"))
        self.date_edit = QDateEdit()
        self.date_edit.setCalendarPopup(True)
        self.date_edit.setDate(QDate.currentDate())
        view_btn = QPushButton("View")
        print_btn = QPushButton("Print")
        view_btn.clicked.connect(self.render_table)
        print_btn.clicked.connect(self.print_report)
        date_row.addWidget(self.date_edit)
        date_row.addWidget(view_btn)
        date_row.addWidget(print_btn)
        date_row.addStretch()
        layout.addLayout(date_row)

        self.table = QTableWidget(0, 5)
        self.table.setHorizontalHeaderLabels(["Invoice#", "Time", "Items", "Amount", "Status"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        layout.addWidget(self.table)

        self.summary_label = QLabel()
        layout.addWidget(self.summary_label)

        bottom_row = QHBoxLayout()
        back_btn = QPushButton("Back")
        back_btn.clicked.connect(main_window.show_dashboard)
        bottom_row.addWidget(back_btn)
        layout.addLayout(bottom_row)

    def refresh(self):
        self.date_edit.setDate(QDate.currentDate())
        self.render_table()

    def render_table(self):
        date_str = self.date_edit.date().toString("yyyy-MM-dd")
        invoices = Invoice.get_by_date(date_str)

        self.table.setRowCount(len(invoices))
        total = 0
        for row, inv in enumerate(invoices):
            time_part = inv["date"].split(" ")[1] if " " in inv["date"] else ""
            self.table.setItem(row, 0, QTableWidgetItem(inv["id"]))
            self.table.setItem(row, 1, QTableWidgetItem(time_part))
            self.table.setItem(row, 2, QTableWidgetItem(str(inv["items_count"])))
            self.table.setItem(row, 3, QTableWidgetItem(f"{inv['total']:.0f}"))
            self.table.setItem(row, 4, QTableWidgetItem("PAID"))
            total += inv["total"]

        count = len(invoices)
        avg = (total / count) if count else 0
        self.summary_label.setText(
            f"Total Sales: {total:.0f} PKR   Invoices: {count}   Avg Sale: {avg:.0f} PKR"
        )

    def print_report(self):
        date_str = self.date_edit.date().toString("yyyy-MM-dd")
        invoices = Invoice.get_by_date(date_str)
        shop_name = get_setting("shop_name")
        port = get_setting("printer_port", "COM4")
        fallback_path = send_report_to_printer(shop_name, date_str, invoices, port)

        if fallback_path:
            QMessageBox.information(
                self, "Printer not responding",
                f"Check cable. Report saved to:\n{fallback_path}",
            )
        else:
            QMessageBox.information(self, "Printed", "Report sent to printer.")
