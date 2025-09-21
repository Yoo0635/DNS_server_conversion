from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QTextEdit, QHBoxLayout
from PyQt5.QtCore import QTimer
import random

class TicketingAccess(QWidget):
    def __init__(self, switch_func):
        super().__init__()
        self.switch_func = switch_func
        self.init_ui()
        self.start_timer()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(12)

        title = QLabel("티켓팅 접속 경로")
        title.setStyleSheet("font-size: 22px; font-weight: bold; color: #0078d7; margin-bottom: 20px;")
        layout.addWidget(title)

        # 접속 경로 정보
        info_text = QTextEdit()
        info_text.setReadOnly(True)
        info_text.setMaximumHeight(200)
        info_text.setStyleSheet("""
            QTextEdit {
                border: 1px solid #ddd;
                border-radius: 5px;
                background-color: #f9f9f9;
                font-size: 14px;
                padding: 10px;
            }
        """)
        
        info_content = """
🌐 네트워크 최적화 서비스 접속 경로

📊 대시보드: http://localhost:8000/dashboard
📈 트래픽 모니터링: http://localhost:8000/traffic
🔧 DNS 설정: http://localhost:8000/dns
📋 티켓팅 시스템: http://localhost:8000/tickets

💡 팁: 각 경로는 실시간으로 네트워크 상태를 모니터링합니다.
        """
        info_text.setPlainText(info_content)
        layout.addWidget(info_text)

        # 상태 표시
        status_label = QLabel("서비스 상태: 정상 운영 중")
        status_label.setStyleSheet("font-size: 16px; color: #28a745; font-weight: bold;")
        layout.addWidget(status_label)

        # 버튼 레이아웃
        btn_layout = QHBoxLayout()
        
        refresh_btn = QPushButton("새로고침")
        refresh_btn.setFixedHeight(35)
        refresh_btn.clicked.connect(self.refresh_status)
        
        back_btn = QPushButton("뒤로가기")
        back_btn.setFixedHeight(35)
        back_btn.clicked.connect(lambda: self.switch_func("dashboard"))
        
        btn_layout.addWidget(refresh_btn)
        btn_layout.addWidget(back_btn)
        layout.addLayout(btn_layout)

        self.setLayout(layout)

    def start_timer(self):
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_status)
        self.timer.start(5000)  # 5초마다 상태 업데이트

    def update_status(self):
        # 실제로는 서버 상태를 체크하지만, 여기서는 랜덤으로 시뮬레이션
        statuses = ["정상 운영 중", "점검 중", "일시적 지연", "정상 운영 중"]
        current_status = random.choice(statuses)
        
        # 상태에 따른 색상 변경
        if "정상" in current_status:
            color = "#28a745"
        elif "점검" in current_status:
            color = "#ffc107"
        else:
            color = "#dc3545"
        
        # 상태 라벨 업데이트 (간단한 시뮬레이션)
        pass

    def refresh_status(self):
        # 새로고침 기능
        print("서비스 상태를 새로고침합니다...")
