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

# backend/dns_servers.py의 서버 목록을 가져와야 합니다.
# 현재 DNS 이름 변환을 위해 임시로 여기에 복사해서 사용합니다.
dns_servers = {
    "Google": "8.8.8.8",
    "KT": "168.126.63.1",
    "SKB": "219.250.36.130",
    "LGU+": "164.124.101.2",
    "KISA": "203.248.252.2"
}

class SmartTicketingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("혼잡 상황 대응 스마트 티켓팅 시스템")
        self.root.geometry("1000x800")
        self.root.configure(bg="#222222")

        self.queue = queue.Queue()
        self.root.after(100, self.check_queue)
        
        self.create_widgets()
        
        # 앱 시작 시 현재 DNS 상태를 가져옵니다.
        self.get_current_dns()
        # 콤보박스에 선택된 IP를 저장하기 위한 변수
        self.selected_dns_ip = None

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
        
        # 현재 DNS 상태를 표시할 라벨 추가
        self.current_dns_label = ttk.Label(self.dns_frame, text="현재 DNS: 불러오는 중...", font=("Helvetica", 12, "bold"), foreground="gray")
        self.current_dns_label.pack(pady=5)
        
        # DNS 기능 버튼들
        self.measure_dns_button = ttk.Button(self.dns_frame, text="DNS 측정", command=lambda: measure_dns(self))
        self.measure_dns_button.pack(pady=5)
        
        # 변경할 DNS 서버를 선택할 콤보박스 추가
        self.dns_choice_label = ttk.Label(self.dns_frame, text="변경할 DNS 서버 선택:", font=("Helvetica", 12))
        self.dns_choice_label.pack(pady=(15, 5))
        self.dns_combobox = ttk.Combobox(self.dns_frame, width=37, font=("Helvetica", 12), state="readonly")
        self.dns_combobox.pack(pady=5)

        # 콤보박스에서 항목을 선택했을 때 IP를 저장하는 함수 연결
        self.dns_combobox.bind("<<ComboboxSelected>>", self.on_dns_selected)

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
        self.measure_ip_button = ttk.Button(self.ip_frame, text="IP 응답 속도 측정", command=lambda: self.measure_ip())
        self.measure_ip_button.pack(pady=5)
        self.fixed_ip_entry = ttk.Entry(self.ip_frame, width=40, font=("Helvetica", 12))
        self.fixed_ip_entry.insert(0, "고정할 IP 주소 입력")
        self.fixed_ip_entry.pack(pady=5)
        self.fix_ip_button = ttk.Button(self.ip_frame, text="IP 고정", command=lambda: self.fix_ip())
        self.fix_ip_button.pack(pady=5)
        self.reset_ip_button = ttk.Button(self.ip_frame, text="IP 초기화", command=lambda: self.reset_ip())
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
    
    def on_dns_selected(self, event):
        # 콤보박스 선택 시 호출, 선택된 이름에 해당하는 IP를 저장
        selected_name = self.dns_combobox.get()
        for item in self.last_dns_results:
            display_text = f"{item['DNS 서버 이름']} ({item['평균 응답 시간(ms)']:.2f}ms)"
            if display_text == selected_name:
                self.selected_dns_ip = item['DNS 서버 IP']
                break

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
                    self.last_dns_results = data.get("결과", [])
                    
                    # 콤보박스에 DNS 서버 목록 업데이트 (이름으로 표시)
                    dns_options = [f"{item['DNS 서버 이름']} ({item['평균 응답 시간(ms)']:.2f}ms)" for item in self.last_dns_results]
                    self.dns_combobox['values'] = dns_options
                    if dns_options:
                        self.dns_combobox.set(dns_options[0]) # 첫 번째 항목을 기본값으로 설정
                        self.selected_dns_ip = self.last_dns_results[0]['DNS 서버 IP'] # 첫 번째 IP를 변수에 저장
                        
                    self.dns_result_text.delete(1.0, tk.END)
                    for item in self.last_dns_results:
                        dns_name = item.get("DNS 서버 이름")
                        latency = item.get("평균 응답 시간(ms)")
                        if latency is not None:
                            self.dns_result_text.insert(tk.END, f"[{dns_name}] 응답 시간: {latency:.2f} ms\n")
                        else:
                            self.dns_result_text.insert(tk.END, f"[{dns_name}] 응답 시간: 실패\n")
                    plot_graph(self, self.last_dns_results) 
                    self.measure_dns_button.config(state=tk.NORMAL)
                    
                elif task == "update_dns_change":
                    self.dns_result_text.insert(tk.END, data + "\n")
                    self.change_dns_button.config(state=tk.NORMAL)
                    self.dns_result_text.see(tk.END) # 스크롤을 맨 아래로 이동
                    self.get_current_dns() # DNS 변경 후 상태 업데이트
                    
                elif task == "update_current_dns":
                    # IP 주소를 이름으로 변환하여 표시
                    display_name = data
                    # 현재 DNS 상태를 표시하는 로직
                    for name, ip in dns_servers.items():
                        if ip == data:
                            display_name = name
                            break
                    self.current_dns_label.config(text=f"현재 DNS: {display_name}")
                    
                elif task == "error":
                    self.dns_result_text.insert(tk.END, data + "\n")
                    self.measure_dns_button.config(state=tk.NORMAL)
                    self.change_dns_button.config(state=tk.NORMAL)
                    self.dns_result_text.see(tk.END)
                    
                self.root.update_idletasks()
        except queue.Empty:
            pass
        finally:
            self.root.after(100, self.check_queue)
            
    def get_current_dns(self):
        def run_get_request():
            try:
                response = requests.get("http://127.0.0.1:8000/current-dns")
                if response.status_code == 200:
                    data = response.json()
                    self.queue.put(("update_current_dns", data.get("current_dns")))
                else:
                    self.queue.put(("error", f"백엔드 서버 오류: {response.status_code}"))
            except requests.exceptions.ConnectionError:
                self.queue.put(("error", "오류: 백엔드 서버가 실행 중이지 않습니다."))
        
        threading.Thread(target=run_get_request).start()

    # 아래 함수들은 IP 응답 속도 기능을 위해 남겨둡니다.
    def measure_ip(self):
        pass

    def fix_ip(self):
        pass

    def reset_ip(self):
        pass

if __name__ == "__main__":
    try:
        requests.get("http://127.0.0.1:8000")
        root = tk.Tk()
        app = SmartTicketingApp(root)
        root.mainloop()
    except requests.exceptions.ConnectionError:
        print("백엔드 서버가 실행 중이지 않습니다. 'uvicorn main:app --reload' 명령어를 실행해 주세요.")