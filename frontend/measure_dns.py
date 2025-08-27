# frontend/measure_dns.py

import requests
import threading
import queue
import tkinter as tk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def measure_dns(app_instance):
    app_instance.dns_result_text.delete(1.0, tk.END)
    app_instance.dns_result_text.insert(tk.END, "측정 중...\n")
    # 아래 버튼 이름을 올바르게 수정합니다.
    app_instance.measure_dns_button.config(state=tk.DISABLED)

    domain = app_instance.domain_entry.get()
    if not domain:
        app_instance.dns_result_text.insert(tk.END, "도메인을 입력하세요.")
        app_instance.measure_dns_button.config(state=tk.NORMAL)
        return

    def run_measurement():
        try:
            response = requests.get(f"http://127.0.0.1:8000/measure?domain={domain}&count=5")
            
            if response.status_code == 200:
                data = response.json()
                app_instance.queue.put(("update_dns_results", data))
            else:
                app_instance.queue.put(("error", f"백엔드 서버 오류: {response.status_code}"))
        except requests.exceptions.ConnectionError:
            app_instance.queue.put(("error", "오류: 백엔드 서버가 실행 중이지 않습니다."))

    threading.Thread(target=run_measurement).start()

def plot_graph(app_instance, data):
    for widget in app_instance.graph_frame.winfo_children():
        widget.destroy()

    labels = [item.get("DNS 서버") for item in data]
    values = [item.get("평균 응답 시간(ms)") for item in data]

    fig, ax = plt.subplots(figsize=(8, 4))
    ax.bar(labels, values, color=['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728'])
    ax.set_title("DNS 서버별 평균 응답 시간")
    ax.set_ylabel("응답 시간 (ms)")
    ax.set_ylim(bottom=0)

    canvas = FigureCanvasTkAgg(fig, master=app_instance.graph_frame)
    canvas_widget = canvas.get_tk_widget()
    canvas_widget.pack(expand=True, fill="both")
    canvas.draw()