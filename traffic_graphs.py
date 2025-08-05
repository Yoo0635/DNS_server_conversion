from base_frame import BaseFrame
import tkinter as tk
import random
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class TrafficGraphs(BaseFrame):
    def __init__(self, master, switch_frame_callback):
        super().__init__(master, switch_frame_callback)
        self.configure(bg='#2e3440')

        self.x_data = list(range(30))
        self.y_data = [0] * 30

        plt.style.use('seaborn-v0_8-darkgrid')

        self.fig, self.ax = plt.subplots(figsize=(7,4), dpi=100)
        self.fig.patch.set_facecolor('#2e3440')
        self.ax.set_facecolor('#3b4252')

        self.line, = self.ax.plot(self.x_data, self.y_data, color='#88c0d0', linewidth=2, marker='o', markersize=5)

        self.ax.set_ylim(0, 500)
        self.ax.set_title("DNS Queries Per Second (QPS)", fontsize=16, color='white', pad=15, fontweight='bold')
        self.ax.set_xlabel("Time (seconds)", fontsize=12, color='#d8dee9', labelpad=8)
        self.ax.set_ylabel("Requests", fontsize=12, color='#d8dee9', labelpad=8)

        self.ax.tick_params(axis='x', colors='#d8dee9')
        self.ax.tick_params(axis='y', colors='#d8dee9')

        self.ax.grid(True, color='#4c566a', linestyle='--', linewidth=0.7, alpha=0.7)

        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.after_id = None
        self.update_graph()

    def update_graph(self):
        new_val = random.randint(0, 500)
        self.y_data = self.y_data[1:] + [new_val]
        self.line.set_ydata(self.y_data)
        self.canvas.draw()

        if self.after_id is not None:
            self.after_cancel(self.after_id)

        self.after_id = self.after(1000, self.update_graph)

    def on_destroy(self):
        if self.after_id is not None:
            self.after_cancel(self.after_id)
            self.after_id = None
