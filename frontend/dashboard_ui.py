# frontend/dashboard_ui.py

import tkinter as tk
from tkinter import ttk, messagebox
import threading
from . import api_client
from . import graphs

class DashboardUI(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack(fill=tk.BOTH, expand=1)
        self.create_widgets()
        
    def create_widgets(self):
        # UI 레이아웃을 위한 노트북 위젯 생성
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(pady=10, expand=True, fill='both')

        # 첫 번째 탭 (DNS 최적화)
        self.dns_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.dns_frame, text="DNS 최적화")
        self.create_dns_tab()

        # 두 번째 탭 (티켓 예매) - 추후 구현
        self.ticketing_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.ticketing_frame, text="티켓 예매 (미구현)")

    def create_dns_tab(self):
        # 입력 및 버튼을 위한 프레임
        input_frame = tk.Frame(self.dns_frame, pady=10)
        input_frame.pack(fill=tk.X)

        tk.Label(input_frame, text="도메인 입력:", font=('Helvetica', 12)).pack(side=tk.LEFT, padx=10)
        self.domain_entry = tk.Entry(input_frame, width=30, font=('Helvetica', 12))
        self.domain_entry.insert(0, "google.com")
        self.domain_entry.pack(side=tk.LEFT, padx=10)

        # DNS 측정 버튼
        dns_button = tk.Button(input_frame, text="DNS 서버 응답 시간 측정", command=self.on_dns_measure, font=('Helvetica', 10))
        dns_button.pack(side=tk.LEFT, padx=5)

        # IP 속도 측정 버튼
        ip_button = tk.Button(input_frame, text="IP 응답 속도 측정", command=self.on_ip_measure, font=('Helvetica', 10))
        ip_button.pack(side=tk.LEFT, padx=5)

        # 그래프를 표시할 프레임
        self.graph_frame = tk.Frame(self.dns_frame)
        self.graph_frame.pack(fill=tk.BOTH, expand=1)
        
        # 상태 메시지 라벨
        self.status_label = tk.Label(self.dns_frame, text="준비 완료", fg="blue", font=('Helvetica', 12))
        self.status_label.pack(pady=5)

    def on_dns_measure(self):
        domain = self.domain_entry.get()
        if not domain:
            messagebox.showerror("오류", "도메인을 입력하세요.")
            return

        self.status_label.config(text="DNS 응답 시간 측정 중...", fg="orange")
        self.clear_graph_frame()
        
        # UI가 멈추지 않도록 스레드에서 API 호출
        threading.Thread(target=self.run_dns_api, args=(domain,)).start()

    def run_dns_api(self, domain):
        data = api_client.get_dns_measurements(domain)
        self.master.after(0, self.display_dns_results, data)

    def display_dns_results(self, data):
        if 'error' in data:
            self.status_label.config(text="API 호출 실패", fg="red")
            messagebox.showerror("오류", f"API 호출에 실패했습니다: {data['error']}")
            return
        
        graphs.create_dns_bar_chart(self.graph_frame, data['결과'])
        self.status_label.config(text="DNS 응답 시간 측정 완료", fg="green")

    def on_ip_measure(self):
        domain = self.domain_entry.get()
        if not domain:
            messagebox.showerror("오류", "도메인을 입력하세요.")
            return
            
        self.status_label.config(text="IP 응답 속도 측정 중...", fg="orange")
        self.clear_graph_frame()

        threading.Thread(target=self.run_ip_api, args=(domain,)).start()

    def run_ip_api(self, domain):
        data = api_client.get_fastest_ip(domain)
        self.master.after(0, self.display_ip_results, data)

    def display_ip_results(self, data):
        if 'error' in data:
            self.status_label.config(text="API 호출 실패", fg="red")
            messagebox.showerror("오류", f"API 호출에 실패했습니다: {data['error']}")
            return

        graphs.create_ip_bar_chart(self.graph_frame, data['전체 결과'])
        self.status_label.config(text="IP 응답 속도 측정 완료", fg="green")

    def clear_graph_frame(self):
        for widget in self.graph_frame.winfo_children():
            widget.destroy()