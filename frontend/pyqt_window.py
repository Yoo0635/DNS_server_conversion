from typing import Optional
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QLineEdit,
    QApplication, QSpinBox, QComboBox, QDialog, QVBoxLayout, QHBoxLayout,
    QMessageBox, QInputDialog
)
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from . import api_client
from .pyqt_charts import canvas_dns, canvas_ip
from backend.admin_check import AdminChecker


QSS = """
QWidget { background: #ffffff; color: #1f2937; }
QPushButton { background: #1f2937; color: white; border: 0px; padding: 8px 14px; border-radius: 6px; }
QPushButton:hover { background: #374151; }
QPushButton:pressed { background: #4b5563; }
QLineEdit { border: 2px solid #e5e7eb; border-radius: 6px; padding: 6px 10px; }
QComboBox { border: 2px solid #e5e7eb; border-radius: 6px; padding: 6px 10px; min-width: 120px; }
QComboBox::drop-down { border: none; }
QComboBox::down-arrow { width: 12px; height: 12px; }
QSpinBox { border: 2px solid #e5e7eb; border-radius: 6px; padding: 4px 8px; min-width: 90px; }
QSpinBox::up-button, QSpinBox::down-button { width: 18px; background: #f3f4f6; border-left: 1px solid #d1d5db; }
QSpinBox::up-button:hover, QSpinBox::down-button:hover { background: #e5e7eb; }
QSpinBox::up-button:pressed, QSpinBox::down-button:pressed { background: #d1d5db; }
QSpinBox::up-arrow, QSpinBox::down-arrow { width: 10px; height: 10px; }
QLabel#status { color: #10b981; font-weight: 600; }
"""


class AdminPasswordDialog(QDialog):
    """관리자 비밀번호 입력 다이얼로그"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("관리자 권한 요청")
        self.setModal(True)
        self.resize(400, 200)
        self.setStyleSheet(QSS)
        
        layout = QVBoxLayout(self)
        
        # 설명 라벨
        info_label = QLabel("""
        🔐 DNS 설정을 위해 관리자 권한이 필요합니다.
        
        관리자 비밀번호를 입력해주세요.
        (비밀번호는 화면에 표시되지 않습니다)
        
        ⚠️ 주의: 이 프로그램은 안전한 DNS 서버만 사용합니다.
        """)
        info_label.setWordWrap(True)
        layout.addWidget(info_label)
        
        # 비밀번호 입력
        self.password_edit = QLineEdit()
        self.password_edit.setEchoMode(QLineEdit.Password)
        self.password_edit.setPlaceholderText("관리자 비밀번호를 입력하세요")
        layout.addWidget(self.password_edit)
        
        # 버튼
        button_layout = QHBoxLayout()
        self.ok_button = QPushButton("확인")
        self.cancel_button = QPushButton("취소")
        
        self.ok_button.clicked.connect(self.accept)
        self.cancel_button.clicked.connect(self.reject)
        
        button_layout.addWidget(self.ok_button)
        button_layout.addWidget(self.cancel_button)
        layout.addLayout(button_layout)
        
        # 엔터키로 확인
        self.password_edit.returnPressed.connect(self.accept)
    
    def get_password(self):
        """입력된 비밀번호 반환"""
        return self.password_edit.text()


class ApiWorker(QThread):
    done = pyqtSignal(dict)
    def __init__(self, kind: str, domain: str = "", count: int = 3, server_name: str = ""):
        super().__init__()
        self.kind = kind
        self.domain = domain
        self.count = count
        self.server_name = server_name
    def run(self):
        if self.kind == 'dns':
            data = api_client.get_dns_measurements(self.domain, self.count)
        elif self.kind == 'ip':
            data = api_client.get_fastest_ip(self.domain)
        elif self.kind == 'analysis':
            # 분석은 먼저 DNS 결과를 받아 전달하고, IP는 UI 스레드에서 후속 호출
            data = api_client.get_dns_measurements(self.domain, self.count)
        elif self.kind == 'apply_dns':
            data = api_client.apply_dns_server(self.server_name)
        elif self.kind == 'reset_dns':
            data = api_client.reset_dns_server()
        else:
            data = {'error': 'unknown kind'}
        self.done.emit(data or {'error': 'empty response'})


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Network Performance Optimizer (PyQt5)')
        self.setStyleSheet(QSS)
        self.resize(1100, 700)

        self._worker: Optional[ApiWorker] = None

        root = QVBoxLayout(self)

        # Top controls
        top = QHBoxLayout()
        self.url_edit = QLineEdit(self)
        self.url_edit.setPlaceholderText('Target URL (e.g., https://tickets.interpark.com/goods/25005777)')
        self.apply_url_btn = QPushButton('Apply URL', self)
        self.apply_url_btn.clicked.connect(self.on_apply_url)
        self.domain_edit = QLineEdit(self)
        self.domain_edit.setPlaceholderText('Domain (e.g., tickets.interpark.com)')
        self.count_spin = QSpinBox(self)
        self.count_spin.setRange(1, 20)
        self.count_spin.setValue(3)
        top.addWidget(self.url_edit, 3)
        top.addWidget(self.apply_url_btn)
        top.addWidget(self.domain_edit, 2)
        top.addWidget(QLabel('Count:', self))
        top.addWidget(self.count_spin)

        # DNS Server Selection
        dns_section = QHBoxLayout()
        dns_section.addWidget(QLabel('DNS Server:', self))
        self.dns_combo = QComboBox(self)
        self.dns_combo.addItems(['Google', 'KT', 'SKB', 'LGU', 'KISA'])
        self.dns_combo.setCurrentText('Google')
        self.btn_apply_dns = QPushButton('Apply DNS', self)
        self.btn_reset_dns = QPushButton('Reset DNS', self)
        self.btn_apply_dns.clicked.connect(self.click_apply_dns)
        self.btn_reset_dns.clicked.connect(self.click_reset_dns)
        dns_section.addWidget(self.dns_combo)
        dns_section.addWidget(self.btn_apply_dns)
        dns_section.addWidget(self.btn_reset_dns)
        dns_section.addStretch()

        # Buttons
        btns = QHBoxLayout()
        self.btn_dns = QPushButton('DNS Server Response Time', self)
        self.btn_quick = QPushButton('Quick Test (1x)', self)
        self.btn_ip = QPushButton('IP Response Speed Test', self)
        self.btn_analysis = QPushButton('Comprehensive Analysis', self)
        for b in (self.btn_dns, self.btn_quick, self.btn_ip, self.btn_analysis):
            btns.addWidget(b)

        self.btn_dns.clicked.connect(self.click_dns)
        self.btn_quick.clicked.connect(self.click_quick)
        self.btn_ip.clicked.connect(self.click_ip)
        self.btn_analysis.clicked.connect(self.click_analysis)

        # Status
        self.status = QLabel('Ready - Enter URL then Apply', self)
        self.status.setObjectName('status')
        
        # Admin status
        self.admin_status = QLabel('', self)
        self.update_admin_status()

        # Chart area with spacing for multiple graphs
        self.chart_host = QVBoxLayout()
        self.chart_host.setSpacing(20)  # 그래프 간 간격 추가

        root.addLayout(top)
        root.addLayout(dns_section)
        root.addLayout(btns)
        root.addWidget(self.status)
        root.addWidget(self.admin_status)
        root.addLayout(self.chart_host, 1)

    def set_status(self, text: str, ok: bool = True):
        self.status.setText(text)
        self.status.setStyleSheet('color: #10b981;' if ok else 'color: #ef4444;')
    
    def update_admin_status(self):
        """관리자 권한 상태 업데이트"""
        if AdminChecker.is_admin():
            self.admin_status.setText("🔐 관리자 권한: 활성화 (DNS 설정 가능)")
            self.admin_status.setStyleSheet('color: #10b981; font-weight: 600;')
            self.btn_apply_dns.setEnabled(True)
            self.btn_reset_dns.setEnabled(True)
        else:
            self.admin_status.setText("⚠️ 관리자 권한: 비활성화 (측정 기능만 사용 가능)")
            self.admin_status.setStyleSheet('color: #f59e0b; font-weight: 600;')
            self.btn_apply_dns.setEnabled(True)  # 버튼은 활성화 (클릭 시 권한 요청)
            self.btn_reset_dns.setEnabled(True)  # 버튼은 활성화 (클릭 시 권한 요청)
    
    def request_admin_with_password(self, password: str) -> bool:
        """비밀번호로 관리자 권한 요청"""
        import subprocess
        try:
            # sudo 권한으로 명령어 실행 테스트
            result = subprocess.run(['sudo', '-S', 'true'], 
                                  input=password, text=True, 
                                  capture_output=True)
            return result.returncode == 0
        except Exception:
            return False

    def clear_chart(self):
        while self.chart_host.count():
            item = self.chart_host.takeAt(0)
            w = item.widget()
            if w:
                w.setParent(None)

    def extract_domain(self, url: str) -> str:
        url = url.strip()
        if url.startswith('http://'):
            url = url[7:]
        elif url.startswith('https://'):
            url = url[8:]
        if url.startswith('www.'):
            url = url[4:]
        if '/' in url:
            url = url.split('/')[0]
        if ':' in url:
            url = url.split(':')[0]
        return url

    def on_apply_url(self):
        domain = self.extract_domain(self.url_edit.text())
        self.domain_edit.setText(domain)
        self.set_status(f'URL applied: {domain}', True)

    def start_worker(self, kind: str, count: int):
        domain = self.domain_edit.text().strip()
        if not domain:
            self.set_status('Please enter a domain', False)
            return
        self.set_status('Loading...', True)
        self._worker = ApiWorker(kind, domain, count)
        self._worker.done.connect(lambda d: self.on_api_done(kind, d))
        self._worker.start()

    def on_api_done(self, kind: str, data: dict):
        if not isinstance(data, dict) or 'error' in data:
            self.set_status(f'API failed: {data.get("error", "empty")}', False)
            return
        self.clear_chart()
        if kind == 'dns':
            # 새로운 API 형식: data['records'] 사용
            if 'records' in data:
                canvas = canvas_dns(data['records'])
                self.chart_host.addWidget(canvas)
                self.set_status(f'DNS completed - Fastest: {data.get("fastest_server", "Unknown")}', True)
            else:
                self.set_status('DNS API 응답 형식 오류', False)
        elif kind == 'ip':
            # 새로운 API 형식: data['results'] 사용
            if 'results' in data:
                canvas = canvas_ip(data['results'])
                self.chart_host.addWidget(canvas)
                self.set_status(f'IP completed - Fastest: {data.get("fastest_ip", "Unknown")}', True)
            else:
                self.set_status('IP API 응답 형식 오류', False)
        elif kind == 'analysis':
            # 간단히 DNS 한 번과 IP 한 번 호출하여 두 그래프를 순차로 추가
            # 이미 data는 dns 결과
            if 'records' in data:
                canvas1 = canvas_dns(data['records'])
                self.chart_host.addWidget(canvas1)
                ip = api_client.get_fastest_ip(self.domain_edit.text().strip())
                if isinstance(ip, dict) and 'results' in ip:
                    canvas2 = canvas_ip(ip['results'])
                    self.chart_host.addWidget(canvas2)
                self.set_status('Analysis completed', True)
            else:
                self.set_status('Analysis API 응답 형식 오류', False)

    # Button handlers
    def click_dns(self):
        self.start_worker('dns', self.count_spin.value())

    def click_quick(self):
        self.start_worker('dns', 1)

    def click_ip(self):
        self.start_worker('ip', 1)

    def click_analysis(self):
        # 분석은 먼저 DNS(기본 count)부터 호출
        self.start_worker('analysis', self.count_spin.value())

    def click_apply_dns(self):
        # 관리자 권한 확인
        if not AdminChecker.is_admin():
            # 권한 요청 다이얼로그 표시
            dialog = AdminPasswordDialog(self)
            if dialog.exec_() == QDialog.Accepted:
                password = dialog.get_password()
                if self.request_admin_with_password(password):
                    self.set_status("✅ 관리자 권한 확인됨", True)
                    self.update_admin_status()
                else:
                    self.set_status("❌ 비밀번호가 올바르지 않습니다", False)
                    return
            else:
                self.set_status("DNS 설정이 취소되었습니다", False)
                return
        
        server_name = self.dns_combo.currentText()
        self.set_status(f'Applying DNS server: {server_name}...', True)
        self._worker = ApiWorker('apply_dns', server_name=server_name)
        self._worker.done.connect(lambda d: self.on_dns_apply_done(d))
        self._worker.start()

    def click_reset_dns(self):
        # 관리자 권한 확인
        if not AdminChecker.is_admin():
            # 권한 요청 다이얼로그 표시
            dialog = AdminPasswordDialog(self)
            if dialog.exec_() == QDialog.Accepted:
                password = dialog.get_password()
                if self.request_admin_with_password(password):
                    self.set_status("✅ 관리자 권한 확인됨", True)
                    self.update_admin_status()
                else:
                    self.set_status("❌ 비밀번호가 올바르지 않습니다", False)
                    return
            else:
                self.set_status("DNS 리셋이 취소되었습니다", False)
                return
        
        self.set_status('Resetting DNS server...', True)
        self._worker = ApiWorker('reset_dns')
        self._worker.done.connect(lambda d: self.on_dns_reset_done(d))
        self._worker.start()

    def on_dns_apply_done(self, data: dict):
        if not isinstance(data, dict) or 'error' in data:
            self.set_status(f'DNS apply failed: {data.get("error", "unknown error")}', False)
        else:
            message = data.get('message', 'DNS applied successfully')
            server_name = data.get('server_name', 'Unknown')
            server_ip = data.get('server_ip', 'Unknown')
            self.set_status(f'{message} ({server_name}: {server_ip})', True)

    def on_dns_reset_done(self, data: dict):
        if not isinstance(data, dict) or 'error' in data:
            self.set_status(f'DNS reset failed: {data.get("error", "unknown error")}', False)
        else:
            message = data.get('message', 'DNS reset successfully')
            self.set_status(message, True)


