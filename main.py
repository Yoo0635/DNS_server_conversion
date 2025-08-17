import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QStackedWidget
from dashboard import Dashboard
from traffic_graphs import TrafficGraphs
from dns_status import DNSStatus  # 새로 만든 DNS 상태 화면
from ticketing import TicketingAccess

class MainApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Smart Ticketing System")
        self.resize(900, 600)

        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)

        self.screens = {
            "dashboard": Dashboard(self.switch_screen),
            "traffic": TrafficGraphs(self.switch_screen),
            "dns_status": DNSStatus(self.switch_screen),  # "server" 대신 "dns_status"
            "ticketing": TicketingAccess(self.switch_screen)
        }

        for screen in self.screens.values():
            self.stack.addWidget(screen)

        self.switch_screen("dashboard")

    def switch_screen(self, name):
        widget = self.screens.get(name)
        if widget:
            self.stack.setCurrentWidget(widget)
        else:
            print(f"Cannot switch to {name}: screen not found")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainApp()
    window.show()
    sys.exit(app.exec())
