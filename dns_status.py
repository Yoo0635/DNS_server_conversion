from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QProgressBar, QHBoxLayout, QSizePolicy
from PyQt5.QtCore import QTimer
import random

class DNSStatus(QWidget):
    def __init__(self, switch_func):
        super().__init__()
        self.switch_func = switch_func
        self.init_ui()
        self.start_timer()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(10, 10, 10, 10)  # 창 여백 좀 줄임
        layout.setSpacing(12)  # 위아래 간격 넉넉히

        title = QLabel("Server Load Gauge")
        title.setStyleSheet("font-size: 22px; font-weight: bold; color: #0078d7; margin-bottom: 20px;")
        layout.addWidget(title)

        self.servers = {
            "Google": "8.8.8.8",
            "KT": "168.126.63.1",
            "SKB": "219.250.36.130",
            "LGU+": "164.124.101.2",
            "KISA": "203.248.252.2"
        }
        self.bars = []

        for name, ip in self.servers.items():
            h_layout = QHBoxLayout()
            h_layout.setSpacing(15)

            label = QLabel(f"{name} ({ip})")
            label.setFixedWidth(140)  # 이름+IP 너비 고정
            label.setStyleSheet("font-size: 14px;")
            h_layout.addWidget(label)

            bar = QProgressBar()
            bar.setMaximum(100)
            bar.setTextVisible(True)
            bar.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            bar.setFixedHeight(22)  # 바 높이 살짝 키움
            bar.setStyleSheet("""
                QProgressBar {
                    border: 1px solid #bbb;
                    border-radius: 5px;
                    background-color: #eee;
                }
                QProgressBar::chunk {
                    background-color: #0078d7;
                    border-radius: 5px;
                }
            """)
            h_layout.addWidget(bar)
            layout.addLayout(h_layout)
            self.bars.append(bar)

        back_btn = QPushButton("Back")
        back_btn.setFixedHeight(35)
        back_btn.clicked.connect(lambda: self.switch_func("dashboard"))
        layout.addWidget(back_btn)

        self.setLayout(layout)

    def start_timer(self):
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_gauges)
        self.timer.start(3000)

    def update_gauges(self):
        for bar in self.bars:
            bar.setValue(random.randint(0, 100))
