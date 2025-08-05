import tkinter as tk
from tkinter import messagebox

from traffic_graphs import TrafficGraphs
from server_status import ServerStatus
from ticketing import TicketingAccess

class Dashboard(tk.Frame):
    def __init__(self, master, switch_frame_callback):
        super().__init__(master)
        self.configure(bg='#2e3440')

        title = tk.Label(self, text="스마트 티켓팅 시스템 대시보드", 
                         font=("Arial", 20, "bold"), fg='white', bg='#2e3440')
        title.pack(pady=20)

        summary_text = (
            "총 DNS 요청: 12,345건\n"
            "활성 서버 수: 5\n"
            "평균 응답 시간: 120ms\n"
            "최적 서버: server3"
        )
        summary_label = tk.Label(self, text=summary_text,
                                 font=("Arial", 14), fg='white', bg='#2e3440', justify=tk.LEFT)
        summary_label.pack(pady=10)

        btn_frame = tk.Frame(self, bg='#2e3440')
        btn_frame.pack(pady=30)

        btn_traffic = tk.Button(btn_frame, text="트래픽 그래프 보기", width=20,
                                command=lambda: switch_frame_callback("traffic"))
        btn_traffic.grid(row=0, column=0, padx=10)

        btn_server = tk.Button(btn_frame, text="서버 상태 확인", width=20,
                               command=lambda: switch_frame_callback("server"))
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

        self.container = tk.Frame(self, bg='#2e3440')
        self.container.pack(fill=tk.BOTH, expand=True)

        self.frames = {}

        self.show_frame("dashboard")

        # 종료시 프레임 종료 예약 콜백 처리
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

    def show_frame(self, name):
        print(f"show_frame 호출: {name}")  # 로그 확인용

        # 현재 화면이 이미 떠있는 경우 숨기기
        for frame_name, frame in self.frames.items():
            if frame_name == name:
                frame.pack(fill=tk.BOTH, expand=True)
            else:
                frame.pack_forget()

        # 프레임이 없으면 생성
        if name not in self.frames:
            if name == "dashboard":
                frame = Dashboard(self.container, self.show_frame)
            elif name == "traffic":
                frame = TrafficGraphs(self.container, self.show_frame)
            elif name == "server":
                frame = ServerStatus(self.container, self.show_frame)
            elif name == "ticketing":
                frame = TicketingAccess(self.container, self.show_frame)
            else:
                frame = tk.Label(self.container, text=f"{name} 화면 준비중...", font=("Arial", 20), fg='white', bg='#2e3440')
            frame.pack(fill=tk.BOTH, expand=True)
            self.frames[name] = frame

    def on_closing(self):
        # 앱 종료 시 프레임 on_destroy 호출 후 종료
        for frame in self.frames.values():
            if hasattr(frame, "on_destroy"):
                frame.on_destroy()
            frame.destroy()
        self.destroy()


if __name__ == "__main__":
    app = MainApp()
    app.mainloop()
