from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton
from PyQt5.QtCore import QUrl
from PyQt5.QtGui import QDesktopServices

class TicketingAccess(QWidget):
    def __init__(self, switch_func):
        super().__init__()
        self.switch_func = switch_func
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        title = QLabel("티켓팅 접속 화면")
        title.setStyleSheet("font-size: 20px; font-weight: bold;")
        layout.addWidget(title)

        info_label = QLabel("아래 버튼을 눌러 티켓팅 페이지에 접속하세요.")
        layout.addWidget(info_label)

        open_btn = QPushButton("티켓팅 접속하기")
        open_btn.clicked.connect(self.open_ticketing_page)
        layout.addWidget(open_btn)

        back_btn = QPushButton("뒤로가기")
        back_btn.clicked.connect(lambda: self.switch_func("dashboard"))
        layout.addWidget(back_btn)

        self.setLayout(layout)

    def open_ticketing_page(self):
        url = QUrl("https://ticketing.example.com")  # 실제 티켓팅 URL로 교체
        QDesktopServices.openUrl(url)
