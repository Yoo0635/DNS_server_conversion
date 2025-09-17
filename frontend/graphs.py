from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt
<<<<<<< HEAD
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
=======
import matplotlib.patches as patches
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import platform
from typing import List, Dict, Optional
import tkinter as tk

# 크로스 플랫폼 폰트 설정
def get_platform_font():
    """플랫폼별 최적 폰트 반환"""
    system = platform.system()
    if system == "Darwin":  # macOS
        return "SF Pro Display", "Helvetica Neue"
    elif system == "Windows":
        return "Segoe UI", "Arial"
    else:  # Linux
        return "Ubuntu", "DejaVu Sans"

# 현대적인 색상 팔레트
COLORS = {
    'primary': '#6366f1',      # 인디고
    'secondary': '#8b5cf6',    # 보라
    'success': '#10b981',      # 에메랄드
    'warning': '#f59e0b',      # 앰버
    'danger': '#ef4444',       # 레드
    'info': '#06b6d4',         # 시안
    'dark': '#1f2937',         # 그레이
    'light': '#f8fafc',        # 슬레이트
    'gradient_start': '#667eea',
    'gradient_end': '#764ba2'
}

def setup_modern_style():
    """현대적인 matplotlib 스타일 설정"""
    plt.style.use('default')
    
    # 폰트 설정
    font_family, fallback_font = get_platform_font()
    plt.rcParams.update({
        'font.family': [font_family, fallback_font, 'sans-serif'],
        'font.size': 10,
        'axes.titlesize': 14,
        'axes.labelsize': 12,
        'xtick.labelsize': 10,
        'ytick.labelsize': 10,
        'legend.fontsize': 10,
        'figure.titlesize': 16
    })

def create_dns_performance_chart(parent: tk.Widget, data: List[Dict]) -> FigureCanvasTkAgg:
    """
    DNS 서버별 응답 시간을 현대적인 차트로 시각화
    """
    setup_modern_style()
    
    # 유효한 데이터만 필터링
    valid_data = [item for item in data if item.get('평균 응답 시간(ms)') is not None and item.get('평균 응답 시간(ms)') != float('inf')]
    
    if not valid_data:
        # 빈 데이터 처리
        fig, ax = plt.subplots(figsize=(10, 6), dpi=100)
        ax.text(0.5, 0.5, 'No measurement data available', 
                ha='center', va='center', fontsize=16, color=COLORS['dark'])
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.axis('off')
        
        canvas = FigureCanvasTkAgg(fig, master=parent)
        return canvas
    
    # 응답 시간 기준으로 정렬
    valid_data.sort(key=lambda x: x['평균 응답 시간(ms)'])
    
    servers = [item['DNS 서버'] for item in valid_data]
    response_times = [item['평균 응답 시간(ms)'] for item in valid_data]
    
    # 차트 생성 (크기 증가)
    fig, ax = plt.subplots(figsize=(12, 8), dpi=100)
    
    # 배경 설정
    fig.patch.set_facecolor('#ffffff')
    ax.set_facecolor('#fafafa')
    
    # 색상 그라데이션 생성
    colors = plt.cm.viridis(np.linspace(0, 1, len(servers)))
    
    # 가로 막대 그래프
    bars = ax.barh(servers, response_times, color=colors, height=0.7, 
                   edgecolor='white', linewidth=2)
    
    # 값 표시
    for i, (bar, time) in enumerate(zip(bars, response_times)):
        width = bar.get_width()
        ax.text(width + max(response_times) * 0.01, bar.get_y() + bar.get_height()/2, 
                f'{time:.1f}ms', ha='left', va='center', fontweight='bold', 
                color=COLORS['dark'], fontsize=11)
    
    # 스타일링
    ax.set_title('DNS Server Response Time', fontsize=16, fontweight='bold', 
                color=COLORS['dark'], pad=20)
    ax.set_xlabel('Response Time (ms)', fontsize=12, color=COLORS['dark'])
    
    # 축 스타일링
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color(COLORS['dark'])
    ax.spines['bottom'].set_color(COLORS['dark'])
    
    # 그리드 추가
    ax.grid(True, axis='x', alpha=0.3, linestyle='--', color=COLORS['dark'])
    
    # 최고 성능 강조
    if response_times:
        best_time = min(response_times)
        best_idx = response_times.index(best_time)
        bars[best_idx].set_edgecolor(COLORS['success'])
        bars[best_idx].set_linewidth(3)
    
    plt.tight_layout(pad=3.0)
    
    canvas = FigureCanvasTkAgg(fig, master=parent)
    return canvas

def create_ip_performance_chart(parent: tk.Widget, data: List[Dict]) -> FigureCanvasTkAgg:
    """
    IP 주소별 응답 시간을 현대적인 차트로 시각화
    """
    setup_modern_style()
    
    # 유효한 데이터만 필터링
    valid_data = [item for item in data if item.get('응답속도(ms)') is not None and item.get('응답속도(ms)') != float('inf')]
    
    if not valid_data:
        # 빈 데이터 처리
        fig, ax = plt.subplots(figsize=(10, 6), dpi=100)
        ax.text(0.5, 0.5, 'No measurement data available', 
                ha='center', va='center', fontsize=16, color=COLORS['dark'])
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.axis('off')
        
        canvas = FigureCanvasTkAgg(fig, master=parent)
        return canvas
    
    # IP 주소와 응답 시간 추출
    ips = [item['IP 주소'] for item in valid_data]
    response_times = [item['응답속도(ms)'] for item in valid_data]
    
    # 차트 생성 (크기 증가)
    fig, ax = plt.subplots(figsize=(12, 8), dpi=100)
    
    # 배경 설정
    fig.patch.set_facecolor('#ffffff')
    ax.set_facecolor('#fafafa')
    
    # 색상 그라데이션 생성
    colors = plt.cm.plasma(np.linspace(0, 1, len(ips)))
    
    # 세로 막대 그래프
    bars = ax.bar(ips, response_times, color=colors, width=0.6, 
                  edgecolor='white', linewidth=2)
    
    # 값 표시
    for bar, time in zip(bars, response_times):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2, height + max(response_times) * 0.01, 
                f'{time:.1f}ms', ha='center', va='bottom', fontweight='bold', 
                color=COLORS['dark'], fontsize=10)
    
    # 스타일링
    ax.set_title('IP Address Response Time', fontsize=16, fontweight='bold', 
                color=COLORS['dark'], pad=20)
    ax.set_ylabel('Response Time (ms)', fontsize=12, color=COLORS['dark'])
    ax.set_xlabel('IP Address', fontsize=12, color=COLORS['dark'])
    
    # X축 라벨 회전
    plt.xticks(rotation=45, ha='right')
    
    # 축 스타일링
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color(COLORS['dark'])
    ax.spines['bottom'].set_color(COLORS['dark'])
    
    # 그리드 추가
    ax.grid(True, axis='y', alpha=0.3, linestyle='--', color=COLORS['dark'])
    
    # 최고 성능 강조
    if response_times:
        best_time = min(response_times)
        best_idx = response_times.index(best_time)
        bars[best_idx].set_edgecolor(COLORS['success'])
        bars[best_idx].set_linewidth(3)
    
    plt.tight_layout(pad=3.0)
    
    canvas = FigureCanvasTkAgg(fig, master=parent)
    return canvas

def create_performance_summary_chart(parent: tk.Widget, dns_data: List[Dict], ip_data: List[Dict]) -> FigureCanvasTkAgg:
    """
    DNS와 IP 성능을 종합한 요약 차트
    """
    setup_modern_style()
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 7), dpi=100)
    
    # 배경 설정
    fig.patch.set_facecolor('#ffffff')
    ax1.set_facecolor('#fafafa')
    ax2.set_facecolor('#fafafa')
    
    # DNS 성능 요약
    if dns_data:
        dns_times = [item.get('평균 응답 시간(ms)', 0) for item in dns_data if item.get('평균 응답 시간(ms)') is not None]
        if dns_times:
            ax1.pie([min(dns_times), max(dns_times) - min(dns_times)], 
                   labels=['Best Performance', 'Performance Gap'], 
                   colors=[COLORS['success'], COLORS['warning']],
                   autopct='%1.1f%%', startangle=90)
            ax1.set_title('DNS Performance Distribution', fontweight='bold', color=COLORS['dark'])
    
    # IP 성능 요약
    if ip_data:
        ip_times = [item.get('응답속도(ms)', 0) for item in ip_data if item.get('응답속도(ms)') is not None and item.get('응답속도(ms)') != float('inf')]
        if ip_times:
            ax2.pie([min(ip_times), max(ip_times) - min(ip_times)], 
                   labels=['Best Performance', 'Performance Gap'], 
                   colors=[COLORS['info'], COLORS['danger']],
                   autopct='%1.1f%%', startangle=90)
            ax2.set_title('IP Performance Distribution', fontweight='bold', color=COLORS['dark'])
    
    plt.tight_layout(pad=3.0)
    
    canvas = FigureCanvasTkAgg(fig, master=parent)
    return canvas

# 기존 함수들과의 호환성을 위한 래퍼 함수들
def create_dns_bar_chart(parent: tk.Widget, data: List[Dict]) -> FigureCanvasTkAgg:
    """기존 코드와의 호환성을 위한 래퍼 함수"""
    return create_dns_performance_chart(parent, data)

def create_ip_bar_chart(parent: tk.Widget, data: List[Dict]) -> FigureCanvasTkAgg:
    """기존 코드와의 호환성을 위한 래퍼 함수"""
    return create_ip_performance_chart(parent, data)
>>>>>>> 2e01351 (tkinter기반)
