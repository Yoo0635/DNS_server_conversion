from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QLineEdit, QFrame, QComboBox, QMessageBox, QSizePolicy
from PyQt5.QtCore import QThread, pyqtSignal
import requests
import json
import matplotlib.pyplot as plt

<<<<<<< HEAD
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
=======
import tkinter as tk
from tkinter import ttk, messagebox
import threading
import platform
from . import api_client
from . import graphs

# 현대적인 색상 팔레트
COLORS = {
    'primary': '#6366f1',
    'secondary': '#8b5cf6', 
    'success': '#10b981',
    'warning': '#f59e0b',
    'danger': '#ef4444',
    'info': '#06b6d4',
    'dark': '#1f2937',
    'light': '#f8fafc',
    'bg_primary': '#ffffff',
    'bg_secondary': '#f8fafc',
    'text_primary': '#1f2937',
    'text_secondary': '#6b7280'
}

class ModernButton(tk.Button):
    """현대적인 스타일의 버튼"""
    def __init__(self, parent, **kwargs):
        default_style = {
            'font': ('SF Pro Display', 11, 'normal') if platform.system() == 'Darwin' else ('Segoe UI', 11, 'normal'),
            'relief': 'flat',
            'borderwidth': 0,
            'cursor': 'hand2',
            'bg': '#1f2937',  # 검정색 배경
            'fg': 'white',    # 흰색 글씨
            'activebackground': '#374151',  # 클릭 시 더 밝은 회색
            'activeforeground': 'white'
        }
        default_style.update(kwargs)
        super().__init__(parent, **default_style)
        
        # 원래 배경색 저장
        self._original_bg = self.cget('bg')
        
        # 호버 및 클릭/포커스 효과
        self.bind('<Enter>', self._on_enter)
        self.bind('<Leave>', self._on_leave)
        self.bind('<Button-1>', self._on_click)
        self.bind('<ButtonRelease-1>', self._on_release)
        self.bind('<FocusIn>', self._on_focus_in)
        self.bind('<FocusOut>', self._on_focus_out)
        
    def _on_enter(self, event):
        # 호버 시 밝은 회색
        self.config(bg='#374151')
        self.config(fg='white')
        
    def _on_leave(self, event):
        # 원래 색상으로 복원
        self.config(bg=self._original_bg)
        self.config(fg='white')
        
    def _on_click(self, event):
        # 클릭 시 더 밝은 색
        self.config(bg='#4b5563')
        
    def _on_release(self, event):
        # 클릭 해제 시 호버 색상으로
        self.config(bg='#374151')

    def _on_focus_in(self, event):
        # 포커스가 들어와도 가독성 유지
        self.config(activebackground='#374151', activeforeground='white', fg='white')

    def _on_focus_out(self, event):
        # 포커스가 나가면 원래 색으로 복원
        self.config(bg=self._original_bg, fg='white')

class DashboardUI(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.configure(bg=COLORS['bg_primary'])
        self.pack(fill=tk.BOTH, expand=1)
        
        # 현재 그래프 캔버스 저장
        self.current_canvas = None
        
        self.create_widgets()
        
    def create_widgets(self):
        # 메인 컨테이너
        main_container = tk.Frame(self, bg=COLORS['bg_primary'])
        main_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # 헤더
        self.create_header(main_container)
        
        # 입력 섹션
        self.create_input_section(main_container)
        
        # 버튼 섹션
        self.create_button_section(main_container)
        
        # 그래프 섹션
        self.create_graph_section(main_container)
        
        # 상태 바
        self.create_status_bar(main_container)

    def create_header(self, parent):
        """헤더 섹션 생성"""
        header_frame = tk.Frame(parent, bg=COLORS['bg_primary'])
        header_frame.pack(fill=tk.X, pady=(0, 20))
        
        title_label = tk.Label(
            header_frame,
            text="🌐 Network Performance Optimizer",
            font=('SF Pro Display', 24, 'bold') if platform.system() == 'Darwin' else ('Segoe UI', 24, 'bold'),
            fg=COLORS['text_primary'],
            bg=COLORS['bg_primary']
        )
        title_label.pack()
        
        subtitle_label = tk.Label(
            header_frame,
            text="Measure DNS and IP response times to find the optimal network path",
            font=('SF Pro Display', 12) if platform.system() == 'Darwin' else ('Segoe UI', 12),
            fg=COLORS['text_secondary'],
            bg=COLORS['bg_primary']
        )
        subtitle_label.pack(pady=(5, 0))

    def create_input_section(self, parent):
        """입력 섹션 생성"""
        input_frame = tk.Frame(parent, bg=COLORS['bg_secondary'], relief='flat', bd=1)
        input_frame.pack(fill=tk.X, pady=(0, 20))
        
        # 내부 패딩을 위한 프레임
        inner_frame = tk.Frame(input_frame, bg=COLORS['bg_secondary'])
        inner_frame.pack(fill=tk.X, padx=20, pady=15)
        
        # DNS 서버 선택 라벨
        dns_label = tk.Label(
            inner_frame,
            text="DNS Server:",
            font=('SF Pro Display', 12, 'bold') if platform.system() == 'Darwin' else ('Segoe UI', 12, 'bold'),
            fg=COLORS['text_primary'],
            bg=COLORS['bg_secondary']
        )
        dns_label.pack(side=tk.LEFT, padx=(0, 10))
        
        # DNS 서버 선택 콤보박스
        self.dns_var = tk.StringVar(value="Google")
        dns_servers = ["Google", "KT", "SKB", "LGU+", "KISA"]
        self.dns_combo = tk.OptionMenu(
            inner_frame, 
            self.dns_var, 
            *dns_servers
        )
        self.dns_combo.config(
            font=('SF Pro Display', 12) if platform.system() == 'Darwin' else ('Segoe UI', 12),
            width=15,
            relief='flat',
            bd=1
        )
        self.dns_combo.pack(side=tk.LEFT, padx=(0, 10))
        
        # 도메인 입력 라벨
        domain_label = tk.Label(
            inner_frame,
            text="Domain:",
            font=('SF Pro Display', 12, 'bold') if platform.system() == 'Darwin' else ('Segoe UI', 12, 'bold'),
            fg=COLORS['text_primary'],
            bg=COLORS['bg_secondary']
        )
        domain_label.pack(side=tk.LEFT, padx=(20, 10))
        
        # 도메인 입력 필드
        self.domain_entry = tk.Entry(
            inner_frame,
            width=25,
            font=('SF Pro Display', 12) if platform.system() == 'Darwin' else ('Segoe UI', 12),
            relief='flat',
            bd=1,
            highlightthickness=2,
            highlightcolor=COLORS['primary'],
            highlightbackground=COLORS['text_secondary']
        )
        self.domain_entry.insert(0, "google.com")
        self.domain_entry.pack(side=tk.LEFT, padx=(0, 10))
        
        # 측정 횟수 선택
        count_label = tk.Label(
            inner_frame,
            text="Test Count:",
            font=('SF Pro Display', 12) if platform.system() == 'Darwin' else ('Segoe UI', 12),
            fg=COLORS['text_primary'],
            bg=COLORS['bg_secondary']
        )
        count_label.pack(side=tk.LEFT, padx=(20, 5))
        
        self.count_var = tk.StringVar(value="3")
        count_spinbox = tk.Spinbox(
            inner_frame,
            from_=1,
            to=20,
            textvariable=self.count_var,
            width=5,
            font=('SF Pro Display', 12) if platform.system() == 'Darwin' else ('Segoe UI', 12),
            relief='flat',
            bd=1
        )
        count_spinbox.pack(side=tk.LEFT)
        
        # Apply 버튼 추가
        apply_button = ModernButton(
            inner_frame,
            text="Apply",
            command=self.apply_settings,
            bg='#dc2626',  # 빨간색
            fg='white',
            width=8,
            height=1
        )
        apply_button.pack(side=tk.LEFT, padx=(10, 0))
        
        # 두 번째 줄 추가
        second_row = tk.Frame(input_frame, bg=COLORS['bg_secondary'])
        second_row.pack(fill=tk.X, padx=20, pady=(0, 15))
        
        # 사용자 URL 입력
        url_label = tk.Label(
            second_row,
            text="Target URL:",
            font=('SF Pro Display', 12, 'bold') if platform.system() == 'Darwin' else ('Segoe UI', 12, 'bold'),
            fg=COLORS['text_primary'],
            bg=COLORS['bg_secondary']
        )
        url_label.pack(side=tk.LEFT, padx=(0, 10))
        
        self.url_entry = tk.Entry(
            second_row,
            width=40,
            font=('SF Pro Display', 12) if platform.system() == 'Darwin' else ('Segoe UI', 12),
            relief='flat',
            bd=1,
            highlightthickness=2,
            highlightcolor=COLORS['primary'],
            highlightbackground=COLORS['text_secondary']
        )
        
        # 복붙 기능 활성화
        self.url_entry.bind('<Control-v>', lambda e: self.url_entry.event_generate('<<Paste>>'))
        self.url_entry.bind('<Control-c>', lambda e: self.url_entry.event_generate('<<Copy>>'))
        self.url_entry.bind('<Control-x>', lambda e: self.url_entry.event_generate('<<Cut>>'))
        self.url_entry.insert(0, "ticket.melon.com")
        self.url_entry.pack(side=tk.LEFT, padx=(0, 10))
        
        # URL 적용 버튼
        url_apply_button = ModernButton(
            second_row,
            text="Apply URL",
            command=self.apply_url,
            bg='#059669',  # 초록색
            fg='white',
            width=10,
            height=1
        )
        url_apply_button.pack(side=tk.LEFT, padx=(10, 0))

    def create_button_section(self, parent):
        """버튼 섹션 생성"""
        button_frame = tk.Frame(parent, bg=COLORS['bg_primary'])
        button_frame.pack(fill=tk.X, pady=(0, 20))
        
        # DNS 측정 버튼
        self.dns_button = ModernButton(
            button_frame,
            text="🔍 DNS Server Response Time",
            command=self.on_dns_measure,
            bg=COLORS['info'],
            fg='white',
            width=25,
            height=2
        )
        
        # 빠른 테스트 버튼 추가
        self.quick_test_button = ModernButton(
            button_frame,
            text="⚡ Quick Test (1x)",
            command=self.on_quick_test,
            bg='#f59e0b',
            fg='white',
            width=15,
            height=2
        )
        self.dns_button.pack(side=tk.LEFT, padx=(0, 5))
        self.quick_test_button.pack(side=tk.LEFT, padx=(0, 10))
        
        # IP 측정 버튼
        self.ip_button = ModernButton(
            button_frame,
            text="⚡ IP Response Speed Test",
            command=self.on_ip_measure,
            bg=COLORS['success'],
            fg='white',
            width=25,
            height=2
        )
        self.ip_button.pack(side=tk.LEFT, padx=(0, 10))
        
        # 종합 분석 버튼
        self.analysis_button = ModernButton(
            button_frame,
            text="📊 Comprehensive Analysis",
            command=self.on_analysis,
            bg=COLORS['secondary'],
            fg='white',
            width=25,
            height=2
        )
        self.analysis_button.pack(side=tk.LEFT)

    def create_graph_section(self, parent):
        """그래프 섹션 생성"""
        graph_frame = tk.Frame(parent, bg=COLORS['bg_secondary'], relief='flat', bd=1)
        graph_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 20))
        
        # 그래프 제목
        graph_title = tk.Label(
            graph_frame,
            text="📈 Performance Test Results",
            font=('SF Pro Display', 16, 'bold') if platform.system() == 'Darwin' else ('Segoe UI', 16, 'bold'),
            fg=COLORS['text_primary'],
            bg=COLORS['bg_secondary']
        )
        graph_title.pack(pady=(15, 10))
        
        # 그래프 컨테이너
        self.graph_container = tk.Frame(graph_frame, bg=COLORS['bg_secondary'])
        self.graph_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 20))

    def create_status_bar(self, parent):
        """상태 바 생성"""
        status_frame = tk.Frame(parent, bg=COLORS['bg_primary'], relief='flat', bd=1)
        status_frame.pack(fill=tk.X)
        
        self.status_label = tk.Label(
            status_frame,
            text="✅ Ready - Enter domain and start testing",
            font=('SF Pro Display', 11) if platform.system() == 'Darwin' else ('Segoe UI', 11),
            fg=COLORS['success'],
            bg=COLORS['bg_primary']
        )
        self.status_label.pack(pady=10)

    def clear_graph_frame(self):
        """그래프 프레임 초기화"""
        for widget in self.graph_container.winfo_children():
            widget.destroy()
        self.current_canvas = None

    def update_status(self, message, color=COLORS['text_primary']):
        """상태 메시지 업데이트"""
        self.status_label.config(text=message, fg=color)
    
    def apply_settings(self):
        """설정 적용"""
        try:
            count = int(self.count_var.get())
            if count < 1 or count > 20:
                self.update_status("❌ Test count must be between 1-20", COLORS['danger'])
                return
            
            domain = self.domain_entry.get().strip()
            if not domain:
                self.update_status("❌ Please enter a domain", COLORS['danger'])
                return
            
            self.update_status(f"✅ Settings applied - Domain: {domain}, Count: {count}", COLORS['success'])
        except ValueError:
            self.update_status("❌ Invalid test count", COLORS['danger'])
    
    def apply_url(self):
        """URL 적용"""
        url = self.url_entry.get().strip()
        if not url:
            self.update_status("❌ Please enter a target URL", COLORS['danger'])
            return
        
        # URL을 도메인으로 변환
        domain = self.extract_domain_from_url(url)
        
        # 도메인 입력 필드에 자동으로 설정
        self.domain_entry.delete(0, tk.END)
        self.domain_entry.insert(0, domain)
        
        self.update_status(f"✅ Target URL applied: {domain}", COLORS['success'])
    
    def extract_domain_from_url(self, url):
        """URL에서 도메인만 추출"""
        import re
        
        # http:// 또는 https:// 제거
        if url.startswith('http://'):
            url = url[7:]
        elif url.startswith('https://'):
            url = url[8:]
        
        # www. 제거
        if url.startswith('www.'):
            url = url[4:]
        
        # 경로 제거 (첫 번째 / 이후 모든 것 제거)
        if '/' in url:
            url = url.split('/')[0]
        
        # 포트 번호 제거 (콜론 이후 제거)
        if ':' in url:
            url = url.split(':')[0]
        
        return url

    def on_quick_test(self):
        """빠른 테스트 (1회 측정)"""
        domain = self.domain_entry.get().strip()
        if not domain:
            messagebox.showerror("Input Error", "Please enter a domain.")
            return

        self.update_status("⚡ Quick test in progress...", COLORS['warning'])
        self.clear_graph_frame()
        self.quick_test_button.config(state='disabled')
        
        threading.Thread(target=self.run_quick_test, args=(domain,), daemon=True).start()

    def run_quick_test(self, domain):
        """빠른 테스트 실행 (1회 측정)"""
        data = api_client.get_dns_measurements(domain, 1)
        self.master.after(0, self.display_quick_test_results, data)

    def display_quick_test_results(self, data):
        """빠른 테스트 결과 표시"""
        self.quick_test_button.config(state='normal')

        # 방어 로직: None 또는 비정상 응답 처리
        if data is None or not isinstance(data, dict):
            self.update_status("❌ API 응답이 비어있습니다", COLORS['danger'])
            messagebox.showerror("Error", "API response is empty or invalid.")
            return

        if 'error' in data:
            self.update_status("❌ Quick test failed", COLORS['danger'])
            messagebox.showerror("Error", f"Quick test failed:\n{data['error']}")
            return
        
        try:
            if data['결과']:
                self.current_canvas = graphs.create_dns_performance_chart(self.graph_container, data['결과'])
                self.current_canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
                
                # 최고 성능 서버 표시
                best_server = min(data['결과'], key=lambda x: x.get('평균 응답 시간(ms)', float('inf')))
                self.update_status(f"⚡ Quick test completed - Best: {best_server['DNS 서버']} ({best_server['평균 응답 시간(ms)']:.1f}ms)", COLORS['success'])
            else:
                self.update_status("❌ No test results", COLORS['danger'])
        except Exception as e:
            self.update_status("❌ Quick test failed", COLORS['danger'])
            messagebox.showerror("Error", f"Quick test error:\n{str(e)}")

    def on_dns_measure(self):
        """DNS 측정 시작"""
        domain = self.domain_entry.get().strip()
        if not domain:
            messagebox.showerror("Input Error", "Please enter a domain.")
            return

        try:
            count = int(self.count_var.get())
        except ValueError:
            count = 5

        self.update_status("🔍 Measuring DNS response time...", COLORS['warning'])
        self.clear_graph_frame()
        self.dns_button.config(state='disabled')
        
        threading.Thread(target=self.run_dns_api, args=(domain, count), daemon=True).start()

    def run_dns_api(self, domain, count):
        """DNS API 호출"""
        data = api_client.get_dns_measurements(domain, count)
        self.master.after(0, self.display_dns_results, data)

    def display_dns_results(self, data):
        """DNS 결과 표시"""
        self.dns_button.config(state='normal')

        # 방어 로직: None 또는 비정상 응답 처리
        if data is None or not isinstance(data, dict):
            self.update_status("❌ API 응답이 비어있습니다", COLORS['danger'])
            messagebox.showerror("Error", "API response is empty or invalid.")
            return

        if 'error' in data:
            self.update_status("❌ API call failed", COLORS['danger'])
            messagebox.showerror("Error", f"API call failed:\n{data['error']}")
            return
        
        try:
            self.current_canvas = graphs.create_dns_performance_chart(self.graph_container, data['결과'])
            self.current_canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
            
            # 최고 성능 서버 표시
            if data['결과']:
                best_server = min(data['결과'], key=lambda x: x.get('평균 응답 시간(ms)', float('inf')))
                self.update_status(f"✅ DNS test completed - Best: {best_server['DNS 서버']} ({best_server['평균 응답 시간(ms)']:.1f}ms)", COLORS['success'])
        except Exception as e:
            self.update_status("❌ Graph generation failed", COLORS['danger'])
            messagebox.showerror("Error", f"Error generating graph:\n{str(e)}")

    def on_ip_measure(self):
        """IP 측정 시작"""
        domain = self.domain_entry.get().strip()
        if not domain:
            messagebox.showerror("Input Error", "Please enter a domain.")
            return

        self.update_status("⚡ Measuring IP response speed...", COLORS['warning'])
        self.clear_graph_frame()
        self.ip_button.config(state='disabled')
        
        threading.Thread(target=self.run_ip_api, args=(domain,), daemon=True).start()

    def run_ip_api(self, domain):
        """IP API 호출"""
        data = api_client.get_fastest_ip(domain)
        self.master.after(0, self.display_ip_results, data)

    def display_ip_results(self, data):
        """IP 결과 표시"""
        self.ip_button.config(state='normal')

        # 방어 로직: None 또는 비정상 응답 처리
        if data is None or not isinstance(data, dict):
            self.update_status("❌ API 응답이 비어있습니다", COLORS['danger'])
            messagebox.showerror("Error", "API response is empty or invalid.")
            return

        if 'error' in data:
            self.update_status("❌ API call failed", COLORS['danger'])
            messagebox.showerror("Error", f"API call failed:\n{data['error']}")
            return
        
        try:
            # IP 측정 결과를 그래프로 표시
            if data['전체 결과']:
                self.current_canvas = graphs.create_ip_performance_chart(self.graph_container, data['전체 결과'])
                self.current_canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
                
                # 최고 성능 IP 표시
                best_ip = min(data['전체 결과'], key=lambda x: x.get('응답속도(ms)', float('inf')))
                self.update_status(f"✅ IP test completed - Best: {best_ip['IP 주소']} ({best_ip['응답속도(ms)']:.1f}ms)", COLORS['success'])
            else:
                self.update_status("❌ No IP data available", COLORS['danger'])
        except Exception as e:
            self.update_status("❌ Graph generation failed", COLORS['danger'])
            messagebox.showerror("Error", f"Error generating graph:\n{str(e)}")

    def on_analysis(self):
        """종합 분석 시작"""
        domain = self.domain_entry.get().strip()
        if not domain:
            messagebox.showerror("Input Error", "Please enter a domain.")
            return

        self.update_status("📊 Running comprehensive analysis...", COLORS['warning'])
        self.clear_graph_frame()
        self.analysis_button.config(state='disabled')
        
        threading.Thread(target=self.run_analysis, args=(domain,), daemon=True).start()

    def run_analysis(self, domain):
        """종합 분석 실행"""
        # DNS와 IP 측정을 동시에 실행
        dns_data = api_client.get_dns_measurements(domain, 5)
        ip_data = api_client.get_fastest_ip(domain)
        
        self.master.after(0, self.display_analysis_results, dns_data, ip_data)

    def display_analysis_results(self, dns_data, ip_data):
        """종합 분석 결과 표시"""
        self.analysis_button.config(state='normal')
        
        if 'error' in dns_data or 'error' in ip_data:
            self.update_status("❌ Analysis failed", COLORS['danger'])
            error_msg = dns_data.get('error', '') + ip_data.get('error', '')
            messagebox.showerror("Error", f"Error during analysis:\n{error_msg}")
            return
        
        try:
            self.current_canvas = graphs.create_performance_summary_chart(
                self.graph_container, 
                dns_data.get('결과', []), 
                ip_data.get('전체 결과', [])
            )
            self.current_canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
            
            self.update_status("✅ Comprehensive analysis completed", COLORS['success'])
        except Exception as e:
            self.update_status("❌ Analysis result display failed", COLORS['danger'])
            messagebox.showerror("Error", f"Error displaying analysis results:\n{str(e)}")
>>>>>>> 2e01351 (tkinter기반)
