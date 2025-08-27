# frontend/ticket_ui.py

import tkinter as tk
from tkinter import ttk, scrolledtext
import requests
import json
import threading
import queue
import time

# 우리가 만든 기능 파일들을 가져옵니다. (상대 경로로 수정)
from .measure_dns import measure_dns, plot_graph
from .change_dns import change_dns
from .reset_dns import reset_dns
from .measure_ip import measure_ip
from .fix_ip import fix_ip
from .reset_ip import reset_ip

class SmartTicketingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("혼잡 상황 대응 스마트 티켓팅 시스템")
        self.root.geometry("1000x800")
        self.root.configure(bg="#222222")

        self.queue = queue.Queue()
        self.root.after(100, self.check_queue)
        
        self.create_widgets()

    def create_widgets(self):
        # UI 레이아웃
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(pady=10, expand=True, fill="both")

        # DNS 프레임과 IP 프레임으로 분리
        self.dns_frame = ttk.LabelFrame(self.notebook, text="DNS 최적화", padding=15)
        self.ip_frame = ttk.LabelFrame(self.notebook, text="IP 응답 속도", padding=15)
        self.ticketing_frame = ttk.Frame(self.notebook)
        
        self.notebook.add(self.dns_frame, text="DNS 최적화")
        self.notebook.add(self.ip_frame, text="IP 응답 속도")
        self.notebook.add(self.ticketing_frame, text="스마트 티켓팅")

        # DNS 탭 UI
        self.dns_label = ttk.Label(self.dns_frame, text="DNS 응답 속도 측정", font=("Helvetica", 16))
        self.dns_label.pack(pady=10)
        self.domain_entry = ttk.Entry(self.dns_frame, width=40, font=("Helvetica", 12))
        self.domain_entry.insert(0, "google.com")
        self.domain_entry.pack(pady=5)
        
        # DNS 기능 버튼들
        self.measure_dns_button = ttk.Button(self.dns_frame, text="DNS 측정", command=lambda: measure_dns(self))
        self.measure_dns_button.pack(pady=5)
        self.new_dns_entry = ttk.Entry(self.dns_frame, width=40, font=("Helvetica", 12))
        self.new_dns_entry.insert(0, "새로운 DNS 서버 IP 입력")
        self.new_dns_entry.pack(pady=5)
        self.change_dns_button = ttk.Button(self.dns_frame, text="DNS 변경", command=lambda: change_dns(self))
        self.change_dns_button.pack(pady=5)
        self.reset_dns_button = ttk.Button(self.dns_frame, text="DNS 초기화", command=lambda: reset_dns(self))
        self.reset_dns_button.pack(pady=5)

        self.dns_result_text = scrolledtext.ScrolledText(self.dns_frame, wrap=tk.WORD, width=70, height=10, font=("Helvetica", 10))
        self.dns_result_text.pack(pady=10, padx=10)
        self.graph_frame = ttk.Frame(self.dns_frame)
        self.graph_frame.pack(pady=10, expand=True, fill="both")

        # IP 탭 UI
        self.ip_label = ttk.Label(self.ip_frame, text="IP 응답 속도 측정", font=("Helvetica", 16))
        self.ip_label.pack(pady=10)

        # IP 기능 버튼들
        self.measure_ip_button = ttk.Button(self.ip_frame, text="IP 응답 속도 측정", command=lambda: measure_ip(self))
        self.measure_ip_button.pack(pady=5)
        self.fixed_ip_entry = ttk.Entry(self.ip_frame, width=40, font=("Helvetica", 12))
        self.fixed_ip_entry.insert(0, "고정할 IP 주소 입력")
        self.fixed_ip_entry.pack(pady=5)
        self.fix_ip_button = ttk.Button(self.ip_frame, text="IP 고정", command=lambda: fix_ip(self))
        self.fix_ip_button.pack(pady=5)
        self.reset_ip_button = ttk.Button(self.ip_frame, text="IP 초기화", command=lambda: reset_ip(self))
        self.reset_ip_button.pack(pady=5)

        self.ip_result_text = scrolledtext.ScrolledText(self.ip_frame, wrap=tk.WORD, width=70, height=10, font=("Helvetica", 10))
        self.ip_result_text.pack(pady=10, padx=10)

        # 티켓팅 탭 UI
        self.ticketing_label = ttk.Label(self.ticketing_frame, text="콘서트 티켓 구매", font=("Helvetica", 16))
        self.ticketing_label.pack(pady=10)
        self.seat_label = ttk.Label(self.ticketing_frame, text="좌석 선택: A열 15번", font=("Helvetica", 12))
        self.seat_label.pack(pady=5)
        self.buy_button = ttk.Button(self.ticketing_frame, text="티켓 구매 (테스트)", command=self.buy_ticket)
        self.buy_button.pack(pady=10)
        self.status_label = ttk.Label(self.ticketing_frame, text="상태: 대기 중...", font=("Helvetica", 12), foreground="gray")
        self.status_label.pack(pady=5)
        self.result_label = ttk.Label(self.ticketing_frame, text="", font=("Helvetica", 12, "bold"), foreground="green")
        self.result_label.pack(pady=10)
    
    def buy_ticket(self):
        self.status_label.config(text="상태: 요청 전송 중...", foreground="yellow")
        self.result_label.config(text="")
        
        def simulate_queue():
            queue_time = 1
            for i in range(queue_time):
                self.status_label.config(text=f"상태: 대기열 {i+1}초...", foreground="orange")
                time.sleep(1)
            self.status_label.config(text="상태: 처리 완료", foreground="white")
            self.result_label.config(text="✅ 티켓 구매 성공!", foreground="green")

        threading.Thread(target=simulate_queue).start()

    def check_queue(self):
        try:
            while True:
                task, data = self.queue.get_nowait()
                if task == "update_dns_results":
                    results = data.get("결과", [])
                    self.dns_result_text.delete(1.0, tk.END)
                    for item in results:
                        dns_server = item.get("DNS 서버")
                        latency = item.get("평균 응답 시간(ms)")
                        if latency is not None:
                            self.dns_result_text.insert(tk.END, f"[{dns_server}] 응답 시간: {latency:.2f} ms\n")
                        else:
                            self.dns_result_text.insert(tk.END, f"[{dns_server}] 응답 시간: 실패\n")
                    plot_graph(self, results) 
                    # 아래 버튼 이름을 올바르게 수정합니다.
                    self.measure_dns_button.config(state=tk.NORMAL)
                elif task == "error":
                    self.dns_result_text.insert(tk.END, data)
                    # 아래 버튼 이름을 올바르게 수정합니다.
                    self.measure_dns_button.config(state=tk.NORMAL)
                self.root.update_idletasks()
        except queue.Empty:
            pass
        finally:
            self.root.after(100, self.check_queue)

if __name__ == "__main__":
    try:
        requests.get("http://127.0.0.1:8000")
        root = tk.Tk()
        app = SmartTicketingApp(root)
        root.mainloop()
    except requests.exceptions.ConnectionError:
        print("백엔드 서버가 실행 중이지 않습니다. 'uvicorn main:app --reload' 명령어를 실행해 주세요.")