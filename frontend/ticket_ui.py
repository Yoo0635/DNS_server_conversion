from PyQt5.QtWidgets import QApplication, QMainWindow, QTabWidget, QWidget, QVBoxLayout, QFrame
from PyQt5.QtCore import QSize
import sys

from dashboard_ui import DashboardUI
from graphs import GraphManager

class TicketUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("스마트 티켓팅 시스템")
        self.setGeometry(100, 100, 1000, 700)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QVBoxLayout(self.central_widget)

        self.tab_widget = QTabWidget()
        self.main_layout.addWidget(self.tab_widget)

        # 각 탭에 들어갈 위젯 생성
        self.main_page = QWidget()
        self.dns_page = QWidget()
        self.ip_page = QWidget()

        # 탭 추가
        self.tab_widget.addTab(self.main_page, "메인 예매")
        self.tab_widget.addTab(self.dns_page, "DNS 최적화")
        self.tab_widget.addTab(self.ip_page, "IP 최적화")

        # 각 페이지의 레이아웃 설정
        self.main_page_layout = QVBoxLayout(self.main_page)
        self.dns_page_layout = QVBoxLayout(self.dns_page)
        self.ip_page_layout = QVBoxLayout(self.ip_page)
        
        # 그래프 매니저를 먼저 생성합니다.
        self.graph_manager = GraphManager()

        # DNS 및 IP 대시보드 UI를 각 탭에 추가하고 graph_manager를 전달합니다.
        self.dns_dashboard = DashboardUI("DNS", self.dns_page_layout, self.graph_manager)
        self.ip_dashboard = DashboardUI("IP", self.ip_page_layout, self.graph_manager)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TicketUI()
    window.show()
    sys.exit(app.exec_())