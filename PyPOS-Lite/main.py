import sys

from PyQt6.QtWidgets import QApplication, QMainWindow, QStackedWidget

from config import APP_NAME
from database import init_db
from ui.dashboard import DashboardScreen
from ui.sales import SalesScreen
from ui.inventory import InventoryScreen
from ui.reports import ReportsScreen
from ui.settings import SettingsScreen


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

        for screen in (self.dashboard, self.sales, self.inventory, self.reports, self.settings):
            self.stack.addWidget(screen)

        self.show_dashboard()

    def show_dashboard(self):
        self.dashboard.refresh()
        self.stack.setCurrentWidget(self.dashboard)

    def show_sales(self):
        self.sales.refresh()
        self.stack.setCurrentWidget(self.sales)

    def show_inventory(self):
        self.inventory.refresh()
        self.stack.setCurrentWidget(self.inventory)

    def show_reports(self):
        self.reports.refresh()
        self.stack.setCurrentWidget(self.reports)

    def show_settings(self):
        self.settings.refresh()
        self.stack.setCurrentWidget(self.settings)


def main():
    init_db()
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
