# frontend/ticket_ui.py

import tkinter as tk
from tkinter import ttk, scrolledtext
import requests
import json
import threading
import time
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import queue

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

        self.dns_frame = ttk.Frame(self.notebook)
        self.ticketing_frame = ttk.Frame(self.notebook)
        
        self.notebook.add(self.dns_frame, text="DNS 최적화")
        self.notebook.add(self.ticketing_frame, text="스마트 티켓팅")

        # DNS 탭 UI
        self.dns_label = ttk.Label(self.dns_frame, text="DNS 응답 속도 측정", font=("Helvetica", 16))
        self.dns_label.pack(pady=10)

        self.domain_entry = ttk.Entry(self.dns_frame, width=40, font=("Helvetica", 12))
        self.domain_entry.insert(0, "google.com")
        self.domain_entry.pack(pady=5)

        self.measure_button = ttk.Button(self.dns_frame, text="DNS 서버 응답 시간 측정", command=self.measure_dns)
        self.measure_button.pack(pady=10)

        self.dns_result_text = scrolledtext.ScrolledText(self.dns_frame, wrap=tk.WORD, width=70, height=10, font=("Helvetica", 10))
        self.dns_result_text.pack(pady=10, padx=10)

        # 그래프를 담을 프레임 추가
        self.graph_frame = ttk.Frame(self.dns_frame)
        self.graph_frame.pack(pady=10, expand=True, fill="both")

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
    
    def plot_graph(self, data):
        for widget in self.graph_frame.winfo_children():
            widget.destroy()

        labels = [item.get("DNS 서버") for item in data]
        values = [item.get("평균 응답 시간(ms)") for item in data]

        fig, ax = plt.subplots(figsize=(8, 4))
        ax.bar(labels, values, color=['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728'])
        ax.set_title("DNS 서버별 평균 응답 시간")
        ax.set_ylabel("응답 시간 (ms)")
        ax.set_ylim(bottom=0)

        canvas = FigureCanvasTkAgg(fig, master=self.graph_frame)
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.pack(expand=True, fill="both")
        canvas.draw()
    
    def measure_dns(self):
        self.dns_result_text.delete(1.0, tk.END)
        self.dns_result_text.insert(tk.END, "측정 중...\n")
        self.measure_button.config(state=tk.DISABLED)

        domain = self.domain_entry.get()
        if not domain:
            self.dns_result_text.insert(tk.END, "도메인을 입력하세요.")
            self.measure_button.config(state=tk.NORMAL)
            return

        def run_measurement():
            try:
                # API 주소 수정 부분
                response = requests.get(f"http://127.0.0.1:8000/measure?domain={domain}&count=5")
                
                if response.status_code == 200:
                    data = response.json()
                    self.queue.put(("update_dns_results", data))
                else:
                    self.queue.put(("error", f"백엔드 서버 오류: {response.status_code}"))
            except requests.exceptions.ConnectionError:
                self.queue.put(("error", "오류: 백엔드 서버가 실행 중이지 않습니다."))

        threading.Thread(target=run_measurement).start()

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
                    self.plot_graph(results)
                    self.measure_button.config(state=tk.NORMAL)
                elif task == "error":
                    self.dns_result_text.insert(tk.END, data)
                    self.measure_button.config(state=tk.NORMAL)
                self.root.update_idletasks()
        except queue.Empty:
            pass
        finally:
            self.root.after(100, self.check_queue)

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

if __name__ == "__main__":
    try:
        requests.get("http://127.0.0.1:8000")
        root = tk.Tk()
        app = SmartTicketingApp(root)
        root.mainloop()
    except requests.exceptions.ConnectionError:
        print("백엔드 서버가 실행 중이지 않습니다. 'uvicorn main:app --reload' 명령어를 실행해 주세요.")