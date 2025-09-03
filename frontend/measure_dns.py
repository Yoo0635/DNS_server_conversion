# frontend/measure_dns.py

import requests
import threading
import tkinter as tk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import matplotlib.pyplot as plt

# 그래프를 그리는 함수
def plot_graph(app_instance, results):
    # 기존 그래프 위젯이 있으면 제거합니다.
    for widget in app_instance.graph_frame.winfo_children():
        widget.destroy()

    # 결과가 없으면 그래프를 그리지 않습니다.
    if not results or all(item['평균 응답 시간(ms)'] == float('inf') for item in results):
        no_data_label = tk.Label(app_instance.graph_frame, text="측정 결과가 없습니다.", font=("Helvetica", 12))
        no_data_label.pack(expand=True, fill="both")
        return

    # 그래프 데이터를 준비합니다.
    labels = [item['DNS 서버 이름'] for item in results]
    latencies = [item['평균 응답 시간(ms)'] for item in results]
    
    # 실패한 항목은 제외합니다.
    valid_results = [(name, latency) for name, latency in zip(labels, latencies) if latency != float('inf')]
    if not valid_results:
        no_data_label = tk.Label(app_instance.graph_frame, text="측정 결과가 없습니다.", font=("Helvetica", 12))
        no_data_label.pack(expand=True, fill="both")
        return
        
    valid_labels = [item[0] for item in valid_results]
    valid_latencies = [item[1] for item in valid_results]

    fig = Figure(figsize=(8, 4), dpi=100)
    ax = fig.add_subplot(111)
    
    # 막대 그래프 그리기
    y_pos = np.arange(len(valid_labels))
    ax.barh(y_pos, valid_latencies, align='center')
    ax.set_yticks(y_pos)
    ax.set_yticklabels(valid_labels)
    ax.invert_yaxis()  # 위에서부터 아래로 정렬
    ax.set_xlabel('Average Latency (ms)') # 이 부분을 영어로 변경
    ax.set_title('DNS Server Latency Comparison') # 이 부분을 영어로 변경

    # 그래프를 Tkinter 창에 포함
    canvas = FigureCanvasTkAgg(fig, master=app_instance.graph_frame)
    canvas.draw()
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)


# 백엔드에 DNS 측정 요청을 보내는 함수
def measure_dns(app_instance):
    domain = app_instance.domain_entry.get()
    if not domain:
        app_instance.dns_result_text.delete(1.0, tk.END)
        app_instance.dns_result_text.insert(tk.END, "오류: 도메인을 입력하세요.\n")
        return

    app_instance.dns_result_text.delete(1.0, tk.END)
    app_instance.dns_result_text.insert(tk.END, f"{domain} 도메인의 DNS 응답 속도를 측정 중입니다...\n")
    app_instance.measure_dns_button.config(state=tk.DISABLED)

    def run_measurement_request():
        try:
            response = requests.get(f"http://127.0.0.1:8000/measure?domain={domain}")
            if response.status_code == 200:
                data = response.json()
                app_instance.queue.put(("update_dns_results", data))
            else:
                app_instance.queue.put(("error", f"백엔드 서버 오류: {response.status_code}"))
        except requests.exceptions.ConnectionError:
            app_instance.queue.put(("error", "오류: 백엔드 서버가 실행 중이지 않습니다."))

    threading.Thread(target=run_measurement_request).start()