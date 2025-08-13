from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QProgressBar, QHBoxLayout
from PyQt5.QtCore import QTimer
import random  # 테스트용 랜덤 부하값 생성

class ServerStatus(QWidget):
    def __init__(self, switch_func):
        super().__init__()
        self.switch_func = switch_func
        self.init_ui()
        self.start_timer()

    def init_ui(self):
        self.layout = QVBoxLayout()

        title = QLabel("서버 상태 화면")
        title.setStyleSheet("font-size: 20px; font-weight: bold;")
        self.layout.addWidget(title)

        self.progress_bars = {}
        servers = ["Server A", "Server B", "Server C"]  # 실제 서버 이름으로 교체 가능

        for name in servers:
            row = QHBoxLayout()
            label = QLabel(name)
            progress = QProgressBar()
            progress.setFormat("%p%")
            progress.setValue(0)
            row.addWidget(label)
            row.addWidget(progress)
            self.layout.addLayout(row)
            self.progress_bars[name] = progress

        back_btn = QPushButton("뒤로가기")
        back_btn.clicked.connect(lambda: self.switch_func("dashboard"))
        self.layout.addWidget(back_btn)

        self.setLayout(self.layout)

    def start_timer(self):
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_load)
        self.timer.start(1000)  # 1000ms = 1초 주기

    def update_load(self):
        # TODO: 여기서 실제 API 호출해서 부하 데이터를 받아와야 함
        # 지금은 테스트용 랜덤 값 사용
        for name, progress in self.progress_bars.items():
            new_load = random.randint(0, 100)
            progress.setValue(new_load)
