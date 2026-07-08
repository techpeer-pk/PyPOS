import sys
import traceback

from PyQt6.QtWidgets import QApplication, QMainWindow, QStackedWidget, QMessageBox

from config import APP_NAME
from database import init_db
from ui.dashboard import DashboardScreen
from ui.sales import SalesScreen
from ui.inventory import InventoryScreen
from ui.reports import ReportsScreen
from ui.settings import SettingsScreen, get_setting
from ui.pin_lock import PinLockDialog
from ui.lock_screen import LockScreen
from services.backup import backup_now


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(APP_NAME)
        self.resize(900, 650)

        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)

        self.dashboard = DashboardScreen(self)
        self.sales = SalesScreen(self)
        self.inventory = InventoryScreen(self)
        self.reports = ReportsScreen(self)
        self.settings = SettingsScreen(self)
        self.lock_screen = LockScreen(self)

        for screen in (self.dashboard, self.sales, self.inventory, self.reports, self.settings, self.lock_screen):
            self.stack.addWidget(screen)

        self.show_dashboard()

    def show_dashboard(self):
        self.dashboard.refresh()
        self.stack.setCurrentWidget(self.dashboard)

    def show_sales(self):
        self.sales.refresh()
        self.stack.setCurrentWidget(self.sales)

    def show_inventory(self):
        if not self.verify_pin():
            return
        self.inventory.refresh()
        self.stack.setCurrentWidget(self.inventory)

    def show_reports(self):
        self.reports.refresh()
        self.stack.setCurrentWidget(self.reports)

    def show_settings(self):
        if not self.verify_pin():
            return
        self.settings.refresh()
        self.stack.setCurrentWidget(self.settings)

    def show_lock_screen(self):
        self.stack.setCurrentWidget(self.lock_screen)

    def verify_pin(self):
        correct_pin = get_setting("admin_pin", "1234")
        dialog = PinLockDialog(self, correct_pin)
        dialog.exec()
        return dialog.unlocked

    def closeEvent(self, event):
        try:
            backup_now()
        except Exception:
            pass
        super().closeEvent(event)


def handle_uncaught_exception(exc_type, exc_value, exc_tb):
    traceback.print_exception(exc_type, exc_value, exc_tb)
    QMessageBox.critical(None, "Data error", "Data error. Restart app.")


def main():
    sys.excepthook = handle_uncaught_exception
    init_db()
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
