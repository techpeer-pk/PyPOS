import os

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap

from config import ASSETS_DIR


class LockScreen(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window

        layout = QVBoxLayout(self)
        layout.addStretch()

        icon = QLabel()
        icon.setPixmap(QPixmap(os.path.join(ASSETS_DIR, "lock-large.png")).scaled(
            72, 72, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation
        ))
        icon.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(icon)

        title = QLabel("POS LOCKED")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("font-size: 24px; font-weight: bold; padding: 10px;")
        layout.addWidget(title)

        subtitle = QLabel("Enter Admin PIN to continue")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(subtitle)

        unlock_btn = QPushButton("Unlock")
        unlock_btn.setMinimumHeight(40)
        unlock_btn.setFixedWidth(160)
        unlock_btn.clicked.connect(self.unlock)
        layout.addWidget(unlock_btn, alignment=Qt.AlignmentFlag.AlignCenter)

        layout.addStretch()

    def unlock(self):
        if self.main_window.verify_pin():
            self.main_window.show_dashboard()
