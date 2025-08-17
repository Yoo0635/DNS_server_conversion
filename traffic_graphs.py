from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton
from PyQt5.QtCore import QTimer
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import random

class TrafficGraphs(QWidget):
    def __init__(self, switch_func): #다른 화면으로 바꾸는 역할을 하는 함수(콜백 함수)
        super().__init__()  # 초기화 작업(내부 설정, 화면 생성 등)이 제대로 실행
        self.switch_func = switch_func # TrafficGraphs 안 어디서든 self.switch_func를 호출해서 화면 전환
        self.init_ui()
        self.start_timer()

    def init_ui(self):
        layout = QVBoxLayout()

        title = QLabel("Traffic Graph Screen")
        title.setStyleSheet("font-size: 20px; font-weight: bold;")
        layout.addWidget(title)

        self.fig = Figure(figsize=(5, 4), dpi=100)
        self.canvas = FigureCanvas(self.fig)
        layout.addWidget(self.canvas)

        # 한 번만 축 생성
        self.ax = self.fig.add_subplot(111)

        back_btn = QPushButton("뒤로가기")
        back_btn.clicked.connect(lambda: self.switch_func("dashboard"))
        layout.addWidget(back_btn)

        self.setLayout(layout)

    def start_timer(self):
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_graph)
        self.timer.start(1000)  # 1초마다 호출

    def update_graph(self):
        self.ax.clear()  # 기존 축 내용만 지우기
        x = [1, 2, 3, 4, 5]
        y = [random.randint(0, 20) for _ in x]
        self.ax.plot(x, y, marker='o')
        self.ax.set_title("Real-Time Network Traffic Graph")
        self.ax.set_xlabel("Time")
        self.ax.set_ylabel("Traffic")
        self.canvas.draw()
