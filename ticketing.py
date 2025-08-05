from base_frame import BaseFrame
import tkinter as tk
import random
from tkinter import messagebox

class TicketingAccess(BaseFrame):
    def __init__(self, master, switch_frame_callback=None):
        super().__init__(master, switch_frame_callback)
        self.configure(bg='#2e3440')

        self.servers = ['server1', 'server2', 'server3', 'server4', 'server5']

        self.label_title = tk.Label(self, text="티켓팅 최적 접속 경로", font=("Arial", 18, "bold"), fg="white", bg="#2e3440")
        self.label_title.pack(pady=10)

        self.info_text = tk.Text(self, height=8, bg="#3b4252", fg="white", font=("Arial", 12))
        self.info_text.pack(fill=tk.BOTH, expand=False, padx=20, pady=10)
        self.info_text.config(state=tk.DISABLED)

        self.btn_recommend = tk.Button(self, text="최적 서버 추천 받기", command=self.recommend_server, bg="#88c0d0", fg="#2e3440", font=("Arial", 12, "bold"))
        self.btn_recommend.pack(pady=10)

        self.selected_server_label = tk.Label(self, text="선택된 서버: 없음", font=("Arial", 14), fg="white", bg="#2e3440")
        self.selected_server_label.pack(pady=5)

        self.btn_connect = tk.Button(self, text="선택 서버로 접속하기", command=self.connect_server, bg="#a3be8c", fg="#2e3440", font=("Arial", 12, "bold"))
        self.btn_connect.pack(pady=10)

        self.current_recommend = None

    def recommend_server(self):
        server_status = {s: random.randint(0, 100) for s in self.servers}
        server_traffic = {s: random.randint(0, 500) for s in self.servers}

        sorted_servers = sorted(self.servers, key=lambda s: (server_status[s], server_traffic[s]))
        best_server = sorted_servers[0]
        self.current_recommend = best_server

        info_lines = ["서버 상태 및 트래픽 정보:\n"]
        for s in self.servers:
            info_lines.append(f"{s} - 상태 점수: {server_status[s]}, 트래픽: {server_traffic[s]} QPS")

        info_lines.append(f"\n추천 서버는 '{best_server}' 입니다!")

        self.info_text.config(state=tk.NORMAL)
        self.info_text.delete("1.0", tk.END)
        self.info_text.insert(tk.END, "\n".join(info_lines))
        self.info_text.config(state=tk.DISABLED)

        self.selected_server_label.config(text=f"선택된 서버: {best_server}")

    def connect_server(self):
        if self.current_recommend:
            messagebox.showinfo("접속 시뮬레이션", f"서버 '{self.current_recommend}'에 접속합니다!")
        else:
            messagebox.showwarning("접속 실패", "먼저 최적 서버를 추천받으세요.")

    def on_destroy(self):
        # 필요하면 예약된 작업 취소 등 정리작업 추가
        pass
