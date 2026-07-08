from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
)
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication

from services.license import get_machine_id, activate


class ActivationDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PyPOS-Lite Activation")
        self.setFixedWidth(420)
        self.setModal(True)

        layout = QVBoxLayout(self)

        title = QLabel("ACTIVATION REQUIRED")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("font-size: 18px; font-weight: bold; padding: 8px;")
        layout.addWidget(title)

        info = QLabel(
            "This copy of PyPOS-Lite is not licensed for this PC.\n"
            "Send the Machine ID below to your vendor to get a License Key."
        )
        info.setWordWrap(True)
        info.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(info)

        machine_id_row = QHBoxLayout()
        self.machine_id_field = QLineEdit(get_machine_id())
        self.machine_id_field.setReadOnly(True)
        self.machine_id_field.setStyleSheet("font-size: 16px; font-weight: bold;")
        copy_btn = QPushButton("Copy")
        copy_btn.clicked.connect(self.copy_machine_id)
        machine_id_row.addWidget(QLabel("Machine ID:"))
        machine_id_row.addWidget(self.machine_id_field)
        machine_id_row.addWidget(copy_btn)
        layout.addLayout(machine_id_row)

        layout.addWidget(QLabel("License Key:"))
        self.license_key_input = QLineEdit()
        self.license_key_input.setPlaceholderText("Paste license key here")
        layout.addWidget(self.license_key_input)

        self.error_label = QLabel("")
        self.error_label.setStyleSheet("color: #d33; font-weight: bold;")
        self.error_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.error_label)

        btn_row = QHBoxLayout()
        activate_btn = QPushButton("Activate")
        activate_btn.clicked.connect(self.try_activate)
        exit_btn = QPushButton("Exit")
        exit_btn.clicked.connect(self.reject)
        btn_row.addWidget(activate_btn)
        btn_row.addWidget(exit_btn)
        layout.addLayout(btn_row)

    def copy_machine_id(self):
        QApplication.clipboard().setText(self.machine_id_field.text())

    def try_activate(self):
        key = self.license_key_input.text().strip()
        if not key:
            self.error_label.setText("Enter a license key.")
            return
        if activate(key):
            self.accept()
        else:
            self.error_label.setText("Invalid license key for this PC.")
            self.license_key_input.clear()

    def closeEvent(self, event):
        self.reject()
        super().closeEvent(event)
