from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QHBoxLayout

class Dashboard(QWidget):
    def __init__(self, switch_func):
        super().__init__()
        self.switch_func = switch_func
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        title = QLabel("스마트 티켓팅 시스템 대시보드")
        title.setStyleSheet("font-size: 24px; font-weight: bold;")
        layout.addWidget(title)

        summary = QLabel(
            "총 DNS 요청: 12,345건\n"
            "활성 서버 수: 5\n"
            "평균 응답 시간: 120ms\n"
            "최적 서버: server3"
        )
        layout.addWidget(summary)

        btn_layout = QHBoxLayout()

        btn_traffic = QPushButton("트래픽 그래프 보기")
        btn_traffic.clicked.connect(lambda: self.switch_func("traffic"))

        btn_server = QPushButton("서버 상태 확인")
        btn_server.clicked.connect(lambda: self.switch_func("dns_status"))  # 여기만 수정

        btn_ticketing = QPushButton("티켓팅 접속 경로")
        btn_ticketing.clicked.connect(lambda: self.switch_func("ticketing"))

        btn_layout.addWidget(btn_traffic)
        btn_layout.addWidget(btn_server)
        btn_layout.addWidget(btn_ticketing)

        layout.addLayout(btn_layout)

        self.setLayout(layout)
