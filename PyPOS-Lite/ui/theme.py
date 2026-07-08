"""App-wide visual theme: stylesheet + button drop shadows.

Applied once in main.py so every screen gets a consistent look
without touching individual screen files.
"""
from PyQt6.QtGui import QColor
from PyQt6.QtWidgets import QGraphicsDropShadowEffect, QPushButton

STYLESHEET = """
QWidget {
    background-color: #F4F7FB;
    color: #1F2937;
    font-size: 13px;
}

QPushButton {
    background-color: #2F6FED;
    color: white;
    border: none;
    border-radius: 8px;
    padding: 8px 16px;
    font-weight: 600;
}
QPushButton:hover {
    background-color: #2760D1;
}
QPushButton:pressed {
    background-color: #1F4FB0;
}
QPushButton:disabled {
    background-color: #A9BEEA;
    color: #F0F3FA;
}

QLineEdit, QComboBox {
    background-color: white;
    border: 1px solid #D3DCE8;
    border-radius: 6px;
    padding: 6px 10px;
    selection-background-color: #2F6FED;
}
QLineEdit:focus, QComboBox:focus {
    border: 1px solid #2F6FED;
}

QGroupBox {
    background-color: white;
    border: 1px solid #E1E7F0;
    border-radius: 10px;
    margin-top: 14px;
    padding: 12px;
    font-weight: 600;
}
QGroupBox::title {
    subcontrol-origin: margin;
    left: 12px;
    padding: 0 6px;
    color: #2F6FED;
}

QTableWidget {
    background-color: white;
    border: 1px solid #E1E7F0;
    border-radius: 8px;
    gridline-color: #EEF1F6;
}
QHeaderView::section {
    background-color: #EAF0FB;
    color: #1F2937;
    padding: 6px;
    border: none;
    font-weight: 600;
}
"""


def apply_button_shadows(root_widget):
    """Add a soft drop shadow to every button under root_widget."""
    for btn in root_widget.findChildren(QPushButton):
        effect = QGraphicsDropShadowEffect(btn)
        effect.setBlurRadius(14)
        effect.setOffset(0, 2)
        effect.setColor(QColor(47, 111, 237, 90))
        btn.setGraphicsEffect(effect)
