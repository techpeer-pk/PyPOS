from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton, QGridLayout
from PyQt6.QtCore import Qt


class PinLockDialog(QDialog):
    def __init__(self, parent, correct_pin):
        super().__init__(parent)
        self.correct_pin = correct_pin
        self.entered = ""
        self.unlocked = False

        self.setWindowTitle("Admin PIN Required")
        self.setFixedWidth(280)

        layout = QVBoxLayout(self)

        title = QLabel("Enter Admin PIN")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("font-size: 16px; font-weight: bold; padding: 8px;")
        layout.addWidget(title)

        self.display = QLabel("")
        self.display.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.display.setStyleSheet("font-size: 28px; letter-spacing: 8px; padding: 10px;")
        self.display.setMinimumHeight(50)
        layout.addWidget(self.display)

        self.error_label = QLabel("")
        self.error_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.error_label.setStyleSheet("color: #d33; font-weight: bold;")
        layout.addWidget(self.error_label)

        grid = QGridLayout()
        keys = [
            ("1", 0, 0), ("2", 0, 1), ("3", 0, 2),
            ("4", 1, 0), ("5", 1, 1), ("6", 1, 2),
            ("7", 2, 0), ("8", 2, 1), ("9", 2, 2),
            ("⌫", 3, 0), ("0", 3, 1), ("OK", 3, 2),
        ]
        for label, row, col in keys:
            btn = QPushButton(label)
            btn.setMinimumSize(70, 50)
            btn.setStyleSheet("font-size: 16px;")
            btn.setFocusPolicy(Qt.FocusPolicy.NoFocus)
            if label == "⌫":
                btn.clicked.connect(self.backspace)
            elif label == "OK":
                btn.clicked.connect(self.submit)
            else:
                btn.clicked.connect(lambda checked, d=label: self.add_digit(d))
            grid.addWidget(btn, row, col)
        layout.addLayout(grid)

        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.setFocus()

    def add_digit(self, digit):
        if len(self.entered) >= 6:
            return
        self.entered += digit
        self.display.setText("●" * len(self.entered))
        self.error_label.setText("")

    def backspace(self):
        self.entered = self.entered[:-1]
        self.display.setText("●" * len(self.entered))

    def submit(self):
        if not self.entered:
            return
        if self.entered == self.correct_pin:
            self.unlocked = True
            self.accept()
        else:
            self.error_label.setText("Incorrect PIN")
            self.entered = ""
            self.display.setText("")

    def keyPressEvent(self, event):
        key = event.key()
        if Qt.Key.Key_0 <= key <= Qt.Key.Key_9:
            self.add_digit(str(key - Qt.Key.Key_0))
        elif key == Qt.Key.Key_Backspace:
            self.backspace()
        elif key in (Qt.Key.Key_Return, Qt.Key.Key_Enter):
            self.submit()
        else:
            super().keyPressEvent(event)
