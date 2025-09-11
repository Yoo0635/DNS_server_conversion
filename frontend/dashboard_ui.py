from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QLineEdit, QFrame, QComboBox, QMessageBox, QSizePolicy
from PyQt5.QtCore import QThread, pyqtSignal
import requests
import json
import matplotlib.pyplot as plt

# 백엔드에서 제공되는 DNS 서버 목록을 하드코딩
DNS_SERVERS = {
    "Google": "8.8.8.8",
    "KT": "168.126.63.1",
    "SKB": "219.250.36.130",
    "LGU+": "164.124.101.2",
    "KISA": "203.248.252.2"
}

class Worker(QThread):
    finished = pyqtSignal(dict)
    error = pyqtSignal(str)
    
    def __init__(self, url, params=None):
        super().__init__()
        self.url = url
        self.params = params
    
    def run(self):
        try:
            response = requests.get(self.url, params=self.params)
            response.raise_for_status()
            self.finished.emit(response.json())
        except requests.exceptions.RequestException as e:
            self.error.emit(f"Error: {e}")

class DashboardUI(QWidget):
    def __init__(self, tab_type, parent_layout, graph_manager):
        super().__init__()
        self.tab_type = tab_type
        self.graph_manager = graph_manager
        
        self.main_layout = QVBoxLayout(self)
        parent_layout.addWidget(self)
        
        # UI 스타일시트 적용
        self.setStyleSheet("""
            QPushButton {
                min-width: 80px; /* 버튼 최소 너비 설정 */
                max-width: 120px;
                padding: 5px 10px;
            }
            QComboBox {
                min-width: 150px;
            }
        """)
        
        # 도메인 입력 UI
        self.domain_input_layout = QHBoxLayout()
        self.domain_label = QLabel("도메인 입력:")
        self.domain_entry = QLineEdit("ticket.melon.com")
        self.domain_input_layout.addWidget(self.domain_label)
        self.domain_input_layout.addWidget(self.domain_entry)
        self.main_layout.addLayout(self.domain_input_layout)

        # DNS 서버 선택 및 제어 UI (DNS 탭에만 적용)
        if self.tab_type == "DNS":
            self.dns_control_layout = QVBoxLayout()
            self.dns_combo = QComboBox()
            self.dns_combo.addItems(DNS_SERVERS.keys())
            
            self.dns_button_layout = QHBoxLayout()
            self.change_button = QPushButton("DNS 적용")
            self.reset_button = QPushButton("DNS 초기화")
            self.dns_button_layout.addWidget(self.change_button)
            self.dns_button_layout.addWidget(self.reset_button)
            
            self.dns_control_layout.addWidget(self.dns_combo)
            self.dns_control_layout.addLayout(self.dns_button_layout)
            self.main_layout.addLayout(self.dns_control_layout)
            
            self.change_button.clicked.connect(self.change_dns)
            self.reset_button.clicked.connect(self.reset_dns)

        # 주요 버튼 UI (세로로 정렬)
        self.button_layout = QVBoxLayout()
        self.measure_button = QPushButton("속도 측정")
        self.hide_graph_button = QPushButton("그래프 숨기기")
        self.button_layout.addWidget(self.measure_button)
        self.button_layout.addWidget(self.hide_graph_button)
        self.main_layout.addLayout(self.button_layout)
        
        # 상태 라벨 및 그래프 프레임
        self.status_label = QLabel(f"{tab_type} 상태: 대기 중")
        self.main_layout.addWidget(self.status_label)
        
        self.graph_frame = QFrame()
        self.main_layout.addWidget(self.graph_frame)
        self.graph_frame_layout = QVBoxLayout(self.graph_frame)

        # 시그널 연결
        self.measure_button.clicked.connect(self.measure_speed)
        self.hide_graph_button.clicked.connect(self.hide_graph)
    
    def measure_speed(self):
        domain = self.domain_entry.text()
        url = f"http://127.0.0.1:8000/{'measure' if self.tab_type == 'DNS' else 'ip'}"
        params = {"domain": domain}
        if self.tab_type == 'DNS':
            params['count'] = 5

        self.status_label.setText(f"{self.tab_type} 속도 측정 중...")
        self.measure_button.setEnabled(False)
        
        self.worker = Worker(url, params)
        if self.tab_type == 'DNS':
            self.worker.finished.connect(self.on_measure_dns_finished)
        else:
            self.worker.finished.connect(self.on_measure_ip_finished)
        self.worker.error.connect(self.on_error)
        self.worker.start()

    def on_measure_dns_finished(self, data):
        self.status_label.setText("DNS 속도 측정 완료!")
        self.measure_button.setEnabled(True)
        self.graph_manager.plot_dns_graph(data, self.graph_frame_layout)

    def on_measure_ip_finished(self, data):
        self.status_label.setText("IP 속도 측정 완료!")
        self.measure_button.setEnabled(True)
        self.graph_manager.plot_ip_graph(data, self.graph_frame_layout)
        
    def hide_graph(self):
        self.graph_manager.clear_layout(self.graph_frame_layout)
        self.status_label.setText("그래프가 숨겨졌습니다.")

    def change_dns(self):
        selected_dns_name = self.dns_combo.currentText()
        new_dns_ip = DNS_SERVERS[selected_dns_name]
        try:
            url = "http://127.0.0.1:8000/change-dns"
            payload = {"new_dns": new_dns_ip}
            response = requests.post(url, json=payload)
            response.raise_for_status()
            self.status_label.setText(f"✅ DNS 서버가 {selected_dns_name} ({new_dns_ip})로 변경되었습니다.")
        except requests.exceptions.RequestException as e:
            self.status_label.setText(f"❌ DNS 변경 오류: {e}")

    def reset_dns(self):
        try:
            url = "http://127.0.0.1:8000/reset-dns"
            response = requests.post(url)
            response.raise_for_status()
            self.status_label.setText("✅ DNS 서버가 기본값으로 초기화되었습니다.")
        except requests.exceptions.RequestException as e:
            self.status_label.setText(f"❌ DNS 초기화 오류: {e}")
            
    def on_error(self, msg):
        self.status_label.setText(f"❌ 오류: {msg}")
        self.measure_button.setEnabled(True)