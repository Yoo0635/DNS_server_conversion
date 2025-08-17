from base_frame import BaseFrame
import tkinter as tk
import random
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class ServerStatus(BaseFrame):
    def __init__(self, master, switch_frame_callback=None):
        super().__init__(master, switch_frame_callback)
        self.configure(bg='#2e3440')

        self.servers = ['server1', 'server2', 'server3', 'server4', 'server5']

        self.fig, self.ax = plt.subplots(figsize=(7,4), dpi=100)
        self.fig.patch.set_facecolor('#2e3440')
        self.ax.set_facecolor('#2e3440')

        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.after_id = None
        self.update_chart()

    def update_chart(self):
        self.ax.clear()

        loads = [random.randint(0, 100) for _ in self.servers]

        colors = []
        for load in loads:
            if load < 30:
                colors.append('#a3be8c')
            elif load < 70:
                colors.append('#ebcb8b')
            else:
                colors.append('#bf616a')

        wedges, texts, autotexts = self.ax.pie(
            loads,
            labels=self.servers,
            autopct='%1.1f%%',
            colors=colors,
            startangle=90,
            textprops={'color':'white', 'weight':'bold', 'fontsize':12}
        )

        self.ax.set_title("서버별 부하 게이지", fontsize=18, color='white', pad=20, fontweight='bold')

        self.canvas.draw()

        if self.after_id is not None:
            self.after_cancel(self.after_id)
        self.after_id = self.after(1000, self.update_chart)

    def on_destroy(self):
        if self.after_id is not None:
            self.after_cancel(self.after_id)
            self.after_id = None
