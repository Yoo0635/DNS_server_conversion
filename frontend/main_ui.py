# frontend/main_ui.py

import tkinter as tk
from .dashboard_ui import DashboardUI

# Tkinter 윈도우 생성
root = tk.Tk()
root.title("스마트 티켓팅 시스템")
root.geometry("800x600")

# DashboardUI 클래스를 윈도우에 연결
app = DashboardUI(master=root)

# 메인 루프 시작
app.mainloop()