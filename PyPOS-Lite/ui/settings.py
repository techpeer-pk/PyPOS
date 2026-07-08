from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QLineEdit,
    QComboBox, QGroupBox, QFormLayout, QMessageBox, QFileDialog
)
from PyQt6.QtCore import Qt

from database import get_connection
from config import BACKUP_DIR
from services.backup import backup_now, restore, get_last_backup_time


def get_setting(key, default=""):
    conn = get_connection()
    try:
        row = conn.execute("SELECT value FROM settings WHERE key = ?", (key,)).fetchone()
        return row["value"] if row else default
    finally:
        conn.close()


def set_setting(key, value):
    conn = get_connection()
    try:
        conn.execute(
            "INSERT INTO settings (key, value) VALUES (?, ?) "
            "ON CONFLICT(key) DO UPDATE SET value = excluded.value",
            (key, value),
        )
        conn.commit()
    finally:
        conn.close()


class SettingsScreen(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window

        layout = QVBoxLayout(self)

        title = QLabel("SETTINGS & CONFIG")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("font-size: 20px; font-weight: bold; padding: 10px;")
        layout.addWidget(title)

        shop_form = QFormLayout()
        self.shop_name_input = QLineEdit()
        self.owner_input = QLineEdit()
        self.phone_input = QLineEdit()
        shop_form.addRow("Shop Name:", self.shop_name_input)
        shop_form.addRow("Owner:", self.owner_input)
        shop_form.addRow("Phone:", self.phone_input)
        layout.addLayout(shop_form)

        printer_box = QGroupBox("PRINTER")
        printer_layout = QHBoxLayout(printer_box)
        printer_layout.addWidget(QLabel("Printer Port:"))
        self.printer_combo = QComboBox()
        self.printer_combo.addItems(["COM1", "COM2", "COM3", "COM4", "USB"])
        test_print_btn = QPushButton("Test Print")
        test_print_btn.clicked.connect(self.test_print)
        printer_layout.addWidget(self.printer_combo)
        printer_layout.addWidget(test_print_btn)
        layout.addWidget(printer_box)

        scanner_box = QGroupBox("SCANNER")
        scanner_layout = QHBoxLayout(scanner_box)
        scanner_layout.addWidget(QLabel("Auto-detect:"))
        self.scanner_combo = QComboBox()
        self.scanner_combo.addItems(["Enabled", "Disabled"])
        test_scan_btn = QPushButton("Test Scan")
        test_scan_btn.clicked.connect(self.test_scan)
        scanner_layout.addWidget(self.scanner_combo)
        scanner_layout.addWidget(test_scan_btn)
        layout.addWidget(scanner_box)

        backup_box = QGroupBox("BACKUP")
        backup_layout = QVBoxLayout(backup_box)
        self.last_backup_label = QLabel("Last Backup: -")
        backup_layout.addWidget(self.last_backup_label)
        backup_btn_row = QHBoxLayout()
        backup_now_btn = QPushButton("Backup Now")
        restore_btn = QPushButton("Restore")
        backup_now_btn.clicked.connect(self.do_backup)
        restore_btn.clicked.connect(self.do_restore)
        backup_btn_row.addWidget(backup_now_btn)
        backup_btn_row.addWidget(restore_btn)
        backup_layout.addLayout(backup_btn_row)
        layout.addWidget(backup_box)

        bottom_row = QHBoxLayout()
        save_btn = QPushButton("Save")
        back_btn = QPushButton("Back")
        save_btn.clicked.connect(self.save_settings)
        back_btn.clicked.connect(main_window.show_dashboard)
        bottom_row.addWidget(save_btn)
        bottom_row.addWidget(back_btn)
        layout.addLayout(bottom_row)

        layout.addStretch()

    def refresh(self):
        self.shop_name_input.setText(get_setting("shop_name"))
        self.owner_input.setText(get_setting("owner"))
        self.phone_input.setText(get_setting("phone"))
        port = get_setting("printer_port", "COM4")
        idx = self.printer_combo.findText(port)
        if idx >= 0:
            self.printer_combo.setCurrentIndex(idx)

        last_backup = get_last_backup_time()
        if last_backup:
            self.last_backup_label.setText(f"Last Backup: {last_backup.strftime('%Y-%m-%d %H:%M')}")
        else:
            self.last_backup_label.setText("Last Backup: Never")

    def save_settings(self):
        set_setting("shop_name", self.shop_name_input.text().strip())
        set_setting("owner", self.owner_input.text().strip())
        set_setting("phone", self.phone_input.text().strip())
        set_setting("printer_port", self.printer_combo.currentText())
        QMessageBox.information(self, "Saved", "Settings saved.")

    def test_print(self):
        QMessageBox.information(self, "Test Print", "Printer integration will be connected in Phase 3.")

    def test_scan(self):
        QMessageBox.information(self, "Test Scan", "Scanner integration will be connected in Phase 3.")

    def do_backup(self):
        path = backup_now()
        QMessageBox.information(self, "Backup Complete", f"Backup saved to:\n{path}")
        self.refresh()

    def do_restore(self):
        path, _ = QFileDialog.getOpenFileName(self, "Select Backup File", BACKUP_DIR, "Database Files (*.db)")
        if not path:
            return
        confirm = QMessageBox.question(
            self, "Confirm Restore",
            "This will overwrite current data with the selected backup. Continue?",
        )
        if confirm != QMessageBox.StandardButton.Yes:
            return
        restore(path)
        QMessageBox.information(self, "Restore Complete", "Database restored. Please restart the app.")
