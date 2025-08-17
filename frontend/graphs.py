# frontend/graphs.py

import matplotlib.pyplot as plt
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from PyQt6.QtWidgets import QWidget, QVBoxLayout
import numpy as np

def create_dns_modern_bar_chart(parent: QWidget, data: list):
    """
    DNS 서버별 응답 시간을 현대적인 막대 그래프로 시각화합니다.
    """
    valid_data = [item for item in data if item['평균 응답 시간(ms)'] is not None]

    if not valid_data:
        return FigureCanvas(plt.Figure())
    
    # 응답 시간이 가장 낮은 순서로 정렬
    valid_data.sort(key=lambda x: x['평균 응답 시간(ms)'])
    
    fig, ax = plt.subplots(figsize=(6, 4), dpi=100)
    fig.patch.set_facecolor('none')  # 그래프 배경을 투명하게 설정
    ax.set_facecolor('none') # 플롯 영역 배경을 투명하게 설정

    servers = [item['DNS 서버'] for item in valid_data]
    response_times = [item['평균 응답 시간(ms)'] for item in valid_data]
    y_pos = np.arange(len(servers))

    # 두께감 있는 가로 막대 그래프 그리기
    ax.barh(y_pos, response_times, color='#66b3ff', height=0.6)
    
    # 막대 끝에 값 표시
    for i, time in enumerate(response_times):
        ax.text(time + 5, i, f"{time:.0f}ms", va='center', fontsize=10, color='white')

    # 차트 스타일 설정
    ax.set_yticks(y_pos)
    ax.set_yticklabels(servers, fontsize=10, color='white')
    ax.set_title('DNS 서버별 평균 응답 시간', fontsize=14, fontweight='bold', color='white')
    ax.set_xlabel('응답 시간 (ms)', fontsize=12, color='white')
    
    # 불필요한 테두리와 눈금 제거
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.tick_params(axis='both', which='major', length=0)
    ax.set_xticks([]) # X축 눈금 제거
    
    plt.tight_layout()
    canvas = FigureCanvas(fig)
    return canvas

def create_ip_bar_chart(parent: QWidget, data: list):
    """
    IP 주소별 응답 시간을 보여주는 막대 그래프를 생성하여 PyQt 위젯에 추가합니다.
    """
    fig, ax = plt.subplots(figsize=(6, 4), dpi=100)

    ips = [item['ip'] for item in data]
    response_times = [item['응답속도'] for item in data]

    ax.bar(ips, response_times, color='#90ee90')
    ax.set_title('IP 주소별 응답 속도', fontsize=14, fontweight='bold', color='white')
    ax.set_ylabel('응답 시간 (ms)', fontsize=12, color='white')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.tick_params(axis='both', which='major', labelsize=10, colors='white', labelcolor='white')
    ax.yaxis.grid(True, linestyle='--', alpha=0.7)

    plt.xticks(rotation=45, ha="right", fontsize=10, color='white')
    plt.tight_layout()

    fig.patch.set_facecolor('#222222')
    ax.set_facecolor('#333333')
    ax.spines['bottom'].set_color('white')
    ax.spines['left'].set_color('white')

    canvas = FigureCanvas(fig)
    return canvas