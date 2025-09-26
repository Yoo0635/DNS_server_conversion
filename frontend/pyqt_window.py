"""
Network Performance Optimizer - Main Window
PyQt5 기반 메인 윈도우 UI
"""

import sys
import os
import platform
import json
import tempfile
from typing import Optional

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QLineEdit,
    QApplication, QSpinBox, QComboBox, QDialog, QMessageBox
)
from PyQt5.QtCore import Qt, QThread, pyqtSignal

import api_client
from pyqt_charts import canvas_dns, canvas_ip

# Backend 모듈 경로 추가
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'backend'))
# AdminChecker 제거됨 - UAC로 대체


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


# AdminPasswordDialog 제거됨 - UAC로 대체


class ApiWorker(QThread):
    """API 호출을 위한 백그라운드 워커"""
    
    done = pyqtSignal(dict)
    
    def __init__(self, kind: str, domain: str = "", count: int = 3, server_name: str = ""):
        super().__init__()
        self.kind = kind
        self.domain = domain
        self.count = count
        self.server_name = server_name
    
    def run(self):
        """API 호출 실행"""
        try:
            if self.kind == 'dns':
                data = api_client.get_dns_measurements(self.domain, self.count)
            elif self.kind == 'ip':
                data = api_client.get_fastest_ip(self.domain)
            elif self.kind == 'analysis':
                # 분석은 먼저 DNS 결과를 받아 전달
                data = api_client.get_dns_measurements(self.domain, self.count)
            elif self.kind == 'apply_dns':
                data = api_client.apply_dns_server(self.server_name)
            elif self.kind == 'reset_dns':
                data = api_client.reset_dns_server()
            else:
                data = {'error': 'unknown kind'}
            
            self.done.emit(data or {'error': 'empty response'})
        except Exception as e:
            self.done.emit({'error': str(e)})


class MainWindow(QWidget):
    """메인 윈도우 클래스"""
    
    def __init__(self):
        super().__init__()
        self._worker: Optional[ApiWorker] = None
        self._setup_window()
        self._setup_ui()
        self._connect_signals()
        self._restore_state_if_available()
        self.update_admin_status()
    
    def _setup_window(self):
        """윈도우 기본 설정"""
        self.setWindowTitle('Network Performance Optimizer v1.0.0')
        self.setStyleSheet(QSS)
        self.resize(1100, 700)
    
    def _setup_ui(self):
        """UI 구성"""
        root = QVBoxLayout(self)
        
        # 상단 컨트롤
        root.addLayout(self._create_top_controls())
        
        # DNS 서버 선택
        root.addLayout(self._create_dns_section())
        
        # 버튼들
        root.addLayout(self._create_button_section())
        
        # 상태 표시
        root.addWidget(self._create_status_section())
        
        # 차트 영역
        self.chart_host = QVBoxLayout()
        self.chart_host.setSpacing(20)
        root.addLayout(self.chart_host, 1)
    
    def _create_top_controls(self) -> QHBoxLayout:
        """상단 컨트롤 생성"""
        layout = QHBoxLayout()
        
        self.url_edit = QLineEdit()
        self.url_edit.setPlaceholderText('Target URL (e.g., https://example.com)')
        
        self.apply_url_btn = QPushButton('Apply URL')
        
        self.domain_edit = QLineEdit()
        self.domain_edit.setPlaceholderText('Domain (e.g., example.com)')
        
        self.count_spin = QSpinBox()
        self.count_spin.setRange(1, 20)
        self.count_spin.setValue(3)
        
        layout.addWidget(self.url_edit, 3)
        layout.addWidget(self.apply_url_btn)
        layout.addWidget(self.domain_edit, 2)
        layout.addWidget(QLabel('Count:'))
        layout.addWidget(self.count_spin)
        
        return layout
    
    def _create_dns_section(self) -> QHBoxLayout:
        """DNS 서버 선택 섹션 생성"""
        layout = QHBoxLayout()
        
        layout.addWidget(QLabel('DNS Server:'))
        
        self.dns_combo = QComboBox()
        self.dns_combo.addItems(['Google', 'KT', 'SKB', 'LGU', 'KISA'])
        self.dns_combo.setCurrentText('Google')
        
        self.btn_apply_dns = QPushButton('Apply DNS')
        self.btn_reset_dns = QPushButton('Reset DNS')
        
        layout.addWidget(self.dns_combo)
        layout.addWidget(self.btn_apply_dns)
        layout.addWidget(self.btn_reset_dns)
        layout.addStretch()
        
        return layout
    
    def _create_button_section(self) -> QHBoxLayout:
        """버튼 섹션 생성"""
        layout = QHBoxLayout()
        
        self.btn_dns = QPushButton('DNS Server Response Time')
        self.btn_quick = QPushButton('Quick Test (1x)')
        self.btn_ip = QPushButton('IP Response Speed Test')
        self.btn_analysis = QPushButton('Comprehensive Analysis')
        
        for btn in (self.btn_dns, self.btn_quick, self.btn_ip, self.btn_analysis):
            layout.addWidget(btn)
        
        return layout
    
    def _create_status_section(self) -> QWidget:
        """상태 표시 섹션 생성"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        self.status = QLabel('Ready - Enter URL then Apply')
        self.status.setObjectName('status')
        
        self.admin_status = QLabel('')
        
        layout.addWidget(self.status)
        layout.addWidget(self.admin_status)
        
        return widget
    
    def _connect_signals(self):
        """시그널 연결"""
        self.apply_url_btn.clicked.connect(self.on_apply_url)
        self.btn_dns.clicked.connect(self.click_dns)
        self.btn_quick.clicked.connect(self.click_quick)
        self.btn_ip.clicked.connect(self.click_ip)
        self.btn_analysis.clicked.connect(self.click_analysis)
        self.btn_apply_dns.clicked.connect(self.click_apply_dns)
        self.btn_reset_dns.clicked.connect(self.click_reset_dns)

    def set_status(self, text: str, ok: bool = True):
        self.status.setText(text)
        self.status.setStyleSheet('color: #10b981;' if ok else 'color: #ef4444;')
    
    def update_admin_status(self):
        """관리자 권한 상태 업데이트"""
        if platform.system() == "Windows":
            # 설명을 간단하게 표기
            self.admin_status.setText("관리자 권한: 자동 처리 (Windows)")
            self.admin_status.setStyleSheet('color: #10b981; font-weight: 600;')
            self.btn_apply_dns.setEnabled(True)
            self.btn_reset_dns.setEnabled(True)
            return
        # 그 외 플랫폼은 기존 로직 유지 (UAC로 대체)
        self.admin_status.setText("🔐 관리자 권한: 자동 처리")
        self.admin_status.setStyleSheet('color: #10b981; font-weight: 600;')
        self.btn_apply_dns.setEnabled(True)
        self.btn_reset_dns.setEnabled(True)
    
    # ----------------------
    # 상태 저장/복원 유틸리티
    # ----------------------
    def _state_path(self) -> str:
        return os.path.join(tempfile.gettempdir(), 'network_optimizer_state.json')

    def _save_state(self):
        try:
            state = {
                'url': self.url_edit.text(),
                'domain': self.domain_edit.text(),
                'count': int(self.count_spin.value()),
                'dns': self.dns_combo.currentText(),
            }
            with open(self._state_path(), 'w', encoding='utf-8') as f:
                json.dump(state, f, ensure_ascii=False)
        except Exception:
            pass

    def _restore_state_if_available(self):
        try:
            path = self._state_path()
            if os.path.exists(path):
                with open(path, 'r', encoding='utf-8') as f:
                    state = json.load(f)
                if isinstance(state, dict):
                    self.url_edit.setText(state.get('url', ''))
                    self.domain_edit.setText(state.get('domain', ''))
                    if isinstance(state.get('count', None), int):
                        self.count_spin.setValue(state['count'])
                    dns_name = state.get('dns')
                    if dns_name and dns_name in [self.dns_combo.itemText(i) for i in range(self.dns_combo.count())]:
                        self.dns_combo.setCurrentText(dns_name)
                # 복원 후에는 파일 삭제(다음 기동 시 혼동 방지)
                try:
                    os.remove(path)
                except Exception:
                    pass
        except Exception:
            pass
        else:
            self.admin_status.setText("⚠️ 관리자 권한: 비활성화 (측정 기능만 사용 가능)")
            self.admin_status.setStyleSheet('color: #f59e0b; font-weight: 600;')
            self.btn_apply_dns.setEnabled(True)
            self.btn_reset_dns.setEnabled(True)
    
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
        # Windows: 명령 단위 승격 (창 유지)
        if platform.system() == "Windows":
            # UAC 팝업 없이 바로 API 호출 (백엔드에서 netsh 명령만 승격)
            server_name = self.dns_combo.currentText()
            if not server_name:
                self.set_status("❌ DNS 서버를 선택하세요", False)
                return
            
            self.set_status('Applying DNS server...', True)
            self._worker = ApiWorker('apply_dns', server_name=server_name)
            self._worker.done.connect(lambda d: self.on_dns_apply_done(d))
            self._worker.start()
            return
        # macOS/Linux: 비밀번호로 1회 승격 (UAC로 대체)
            # macOS/Linux: 기존 비밀번호 다이얼로그 유지
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
        # Windows: 명령 단위 승격 (창 유지)
        if platform.system() == "Windows":
            # UAC 팝업 없이 바로 API 호출 (백엔드에서 netsh 명령만 승격)
            self.set_status('Resetting DNS server...', True)
            self._worker = ApiWorker('reset_dns')
            self._worker.done.connect(lambda d: self.on_dns_reset_done(d))
            self._worker.start()
            return
        # macOS/Linux: 비밀번호로 1회 승격 (UAC로 대체)
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
            error_msg = data.get("error", "unknown error")
            if "관리자 권한" in error_msg or "sudo" in error_msg.lower():
                # 플랫폼별 안내
                if platform.system() == "Windows":
                    QMessageBox.warning(self, "관리자 권한 필요",
                        "DNS 설정을 위해 관리자 권한이 필요합니다.\n\n"
                        "해결 방법:\n"
                        "1. 프로그램을 '관리자 권한으로 실행'하여 다시 실행\n"
                        "2. 또는 'Apply DNS' 클릭 시 표시되는 UAC 팝업에서 '예' 선택")
                else:
                    QMessageBox.warning(self, "관리자 권한 필요",
                        "DNS 설정을 위해 관리자 권한이 필요합니다.\n\n"
                        "해결 방법:\n"
                        "1. 터미널에서 다음 명령어로 실행:\n"
                        "   sudo python3 run_app.py\n\n"
                        "2. 또는 시스템 설정에서 DNS를 수동으로 변경하세요.")
                self.set_status("❌ 관리자 권한이 필요합니다", False)
            else:
                self.set_status(f'DNS apply failed: {error_msg}', False)
        else:
            message = data.get('message', 'DNS applied successfully')
            server_name = data.get('server_name', 'Unknown')
            server_ip = data.get('server_ip', 'Unknown')
            self.set_status(f'{message} ({server_name}: {server_ip})', True)

    def on_dns_reset_done(self, data: dict):
        if not isinstance(data, dict) or 'error' in data:
            error_msg = data.get("error", "unknown error")
            if "관리자 권한" in error_msg or "sudo" in error_msg.lower():
                # 관리자 권한 오류인 경우 사용자 친화적 메시지 표시
                QMessageBox.warning(self, "관리자 권한 필요", 
                    "DNS 리셋을 위해 관리자 권한이 필요합니다.\n\n"
                    "해결 방법:\n"
                    "1. 터미널에서 다음 명령어로 실행:\n"
                    "   sudo python3 run_app.py\n\n"
                    "2. 또는 시스템 설정에서 DNS를 수동으로 변경하세요.")
                self.set_status("❌ 관리자 권한이 필요합니다", False)
            else:
                self.set_status(f'DNS reset failed: {error_msg}', False)
        else:
            message = data.get('message', 'DNS reset successfully')
            self.set_status(message, True)


