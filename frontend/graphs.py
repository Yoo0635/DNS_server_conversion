from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt
from PyQt5.QtWidgets import QVBoxLayout

class GraphManager:
    def __init__(self):
        pass # 더 이상 레이아웃을 받지 않고, plot 함수에서 직접 받습니다.
        
    def clear_layout(self, layout):
        while layout.count():
            child = layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

    def plot_dns_graph(self, data, parent_layout):
        self.clear_layout(parent_layout)
        
        fig, ax = plt.subplots(figsize=(6, 4))
        
        labels = [d['DNS 서버 이름'] for d in data['결과']]
        times = [d['평균 응답 시간(ms)'] for d in data['결과']]
        
        ax.bar(labels, times, color='skyblue')
        ax.set_title("DNS 응답 속도", fontdict={'family': 'Arial'})
        ax.set_xlabel("DNS 서버", fontdict={'family': 'Arial'})
        ax.set_ylabel("평균 응답 시간(ms)", fontdict={'family': 'Arial'})
        ax.tick_params(axis='x', rotation=45)
        
        fig.tight_layout()
        
        canvas = FigureCanvas(fig)
        parent_layout.addWidget(canvas)
        plt.close(fig)

    def plot_ip_graph(self, data, parent_layout):
        self.clear_layout(parent_layout)
        
        fig, ax = plt.subplots(figsize=(6, 4))
        
        labels = [d['ip'] for d in data['전체 결과']]
        times = [d['응답속도'] for d in data['전체 결과']]
        
        ax.bar(labels, times, color='lightgreen')
        ax.set_title("IP 응답 속도", fontdict={'family': 'Arial'})
        ax.set_xlabel("IP 주소", fontdict={'family': 'Arial'})
        ax.set_ylabel("응답 시간(ms)", fontdict={'family': 'Arial'})
        ax.tick_params(axis='x', rotation=45)
        
        fig.tight_layout()
        
        canvas = FigureCanvas(fig)
        parent_layout.addWidget(canvas)
        plt.close(fig)