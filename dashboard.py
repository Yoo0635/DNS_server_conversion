import tkinter as tk
from traffic_graphs import TrafficGraphs
from server_status import ServerStatus
from ticketing import TicketingAccess

class Dashboard(tk.Frame):
    def __init__(self, master, switch_frame_callback):
        super().__init__(master)
        self.configure(bg='#2e3440')

        # 상단 제목
        title = tk.Label(self, text="스마트 티켓팅 시스템 대시보드", 
                         font=("Arial", 20, "bold"), fg='white', bg='#2e3440')
        title.pack(pady=20)

        # 간단 요약 정보 (예시)
        summary_text = (
            "총 DNS 요청: 12,345건\n"
            "활성 서버 수: 5\n"
            "평균 응답 시간: 120ms\n"
            "최적 서버: server3"
        )
        summary_label = tk.Label(self, text=summary_text,
                                 font=("Arial", 14), fg='white', bg='#2e3440', justify=tk.LEFT)
        summary_label.pack(pady=10)

        # 메뉴 버튼
        btn_frame = tk.Frame(self, bg='#2e3440')
        btn_frame.pack(pady=30)

        btn_traffic = tk.Button(btn_frame, text="트래픽 그래프 보기", width=20,
                                command=lambda: switch_frame_callback("traffic_graphs"))
        btn_traffic.grid(row=0, column=0, padx=10)

        btn_server = tk.Button(btn_frame, text="서버 상태 확인", width=20,
                               command=lambda: switch_frame_callback("server_status"))
        btn_server.grid(row=0, column=1, padx=10)

        btn_ticketing = tk.Button(btn_frame, text="티켓팅 접속 경로", width=20,
                                  command=lambda: switch_frame_callback("ticketing"))
        btn_ticketing.grid(row=0, column=2, padx=10)

class MainApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Smart Ticketing System")
        self.geometry("900x600")
        self.configure(bg='#2e3440')

        self.current_frame = None
        self.switch_frame("dashboard")

    def switch_frame(self, frame_name):
        if self.current_frame is not None:
            self.current_frame.destroy()

        if frame_name == "dashboard":
            self.current_frame = Dashboard(self, self.switch_frame)
        elif frame_name == "traffic_graphs":
            self.current_frame = TrafficGraphs(self, self.switch_frame)
        elif frame_name == "server_status":
            self.current_frame = ServerStatus(self, self.switch_frame)
        elif frame_name == "ticketing":
            self.current_frame = TicketingAccess(self, self.switch_frame)
        else:
            self.current_frame = tk.Label(self, text=f"{frame_name} 화면 준비중...", 
                                          font=("Arial", 20), fg='white', bg='#2e3440')

        self.current_frame.pack(fill="both", expand=True)

if __name__ == "__main__":
    app = MainApp()
    app.mainloop()
