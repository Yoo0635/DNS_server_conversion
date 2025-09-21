from typing import List, Dict  # 'List'와 'Dict' 타입을 사용하기 위해 불러옵니다.
import numpy as np  # 수학적 연산을 위해 넘파이(numpy) 라이브러리를 불러옵니다.
import matplotlib.pyplot as plt  # 그래프를 그리기 위해 matplotlib의 pyplot 모듈을 불러옵니다.
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas  # Qt5 애플리케이션에 그래프를 포함시키기 위한 클래스를 불러옵니다.


PALETTE = {
    'bg': '#ffffff',  # 배경색: 흰색
    'panel': '#f5f7fb',  # 그래프 영역 패널색: 연한 회색
    'text': '#1f2937',  # 텍스트 색상: 진한 회색
    'accent': '#6366f1',  # 강조색: 보라색
    'ok': '#10b981',  # 성공 상태색: 초록색
    'warn': '#f59e0b'  # 경고 상태색: 주황색
}


def _style_matplotlib():
    plt.style.use('default')
    plt.rcParams.update({
        'axes.titlesize': 14,
        'axes.labelsize': 12,
        'xtick.labelsize': 10,
        'ytick.labelsize': 10,
        'figure.titlesize': 16,
        'text.color': PALETTE['text']
    })


def canvas_dns(data: List[Dict]) -> FigureCanvas:  # DNS 서버 응답 시간 그래프를 그리는 함수입니다.
    _style_matplotlib()  # 위에서 정의한 스타일 설정을 적용합니다.

    # 새로운 API 형식에 맞게 데이터 처리
    valid = [d for d in data if d.get('avg') not in (None, float('inf'))]  # 유효한 데이터만 필터링합니다.
    # figsize는 그래프의 가로, 세로 크기(인치)를 설정합니다. (11, 6.5)는 가로 11인치, 세로 6.5인치입니다.
    # dpi는 해상도를 설정하며, 숫자가 높을수록 선명해집니다.
    fig, ax = plt.subplots(figsize=(10, 6), dpi=100, constrained_layout=True)
    fig.patch.set_facecolor(PALETTE['bg'])  # 그래프를 포함하는 전체 영역의 배경색을 설정합니다.
    ax.set_facecolor(PALETTE['panel'])  # 막대 그래프가 그려지는 실제 영역의 배경색을 설정합니다.

    if not valid:  # 유효한 데이터가 없을 경우
        ax.text(0.5, 0.5, 'No data', ha='center', va='center')  # "No data" 텍스트를 그래프 중앙에 표시합니다.
    else:  # 데이터가 있을 경우
        valid.sort(key=lambda x: x['avg'])  # '평균 응답 시간'을 기준으로 데이터를 오름차순 정렬합니다.
        servers = [d['server'] for d in valid]  # DNS 서버 이름 리스트를 만듭니다.
        times = [d['avg'] for d in valid]  # 평균 응답 시간 리스트를 만듭니다.
        colors = plt.cm.viridis(np.linspace(0, 1, len(servers)))  # 막대마다 다른 색상을 적용하기 위한 색상 리스트를 만듭니다.
        # 슬림한 가로 막대: height를 줄이고, 테두리를 살짝 주어 분리감을 높입니다.
        bars = ax.barh(
            servers,
            times,
            height=0.45,
            color=colors,
            edgecolor='#111111',
            linewidth=1.2,
            alpha=0.95
        )
        for b, t in zip(bars, times):  # 각 막대에 응답 시간 텍스트를 추가합니다.
            ax.text(
                b.get_width() + max(times) * 0.015,
                b.get_y() + b.get_height()/2,
                f'{t:.1f}ms',
                va='center',
                fontsize=10
            )  # 막대 끝에 응답 시간을 텍스트로 표시합니다.
        ax.set_title('DNS Server Response Time', pad=16)  # 그래프의 제목을 설정합니다.
        ax.set_xlabel('Response Time (ms)')  # x축의 라벨을 설정합니다.
        ax.grid(True, axis='x', linestyle='--', alpha=0.3)  # x축에 점선 그리드를 표시합니다.

    # constrained_layout로 기본 여백을 확보하고, 상/하단을 약간 더 여유롭게 설정합니다.
    fig.subplots_adjust(top=0.93, bottom=0.18)
    return FigureCanvas(fig)  # Matplotlib 그림 객체를 Qt 위젯으로 변환하여 반환합니다.


def canvas_ip(data: List[Dict]) -> FigureCanvas:  # IP 주소 응답 시간 그래프를 그리는 함수입니다.
    _style_matplotlib()  # 위에서 정의한 스타일 설정을 적용합니다.
    # figsize는 그래프의 가로, 세로 크기(인치)를 설정합니다.
    fig, ax = plt.subplots(figsize=(10, 6), dpi=100, constrained_layout=True)
    fig.patch.set_facecolor(PALETTE['bg'])  # 전체 그림의 배경색을 설정합니다.
    ax.set_facecolor(PALETTE['panel'])  # 그래프 영역의 배경색을 설정합니다.

    # 새로운 API 형식에 맞게 데이터 처리
    valid = [d for d in data if d.get('response_time') not in (None, float('inf'))]  # 유효한 데이터만 필터링합니다.
    if not valid:  # 유효한 데이터가 없을 경우
        ax.text(0.5, 0.5, 'No data', ha='center', va='center')  # "No data" 텍스트를 그래프 중앙에 표시합니다.
    else:  # 데이터가 있을 경우
        # UI 표시용 매핑: IP → 사람이 이해하기 쉬운 공급자명(간단 매핑)
        def map_ip_to_provider(ip: str) -> str:
            ip_l = str(ip)
            if '8.8.' in ip_l or '8.34.' in ip_l:
                return 'Google'
            elif '1.1.1.1' in ip_l:
                return 'Cloudflare'
            return ip_l  # 기본은 그대로 두고, 필요 시 확장

        labels = [map_ip_to_provider(d.get('ip', 'Unknown')) for d in valid]
        times = [d['response_time'] for d in valid]  # 응답 속도 리스트를 만듭니다.
        colors = plt.cm.plasma(np.linspace(0, 1, len(labels)))  # 막대마다 다른 색상을 적용하기 위한 색상 리스트를 만듭니다.
        # 슬림한 세로 막대: width를 줄이고, 테두리를 살짝 추가합니다.
        bars = ax.bar(
            labels,
            times,
            width=0.5,
            color=colors,
            edgecolor='#111111',
            linewidth=1.2,
            alpha=0.95
        )
        for b, t in zip(bars, times):  # 각 막대에 응답 속도 텍스트를 추가합니다.
            ax.text(b.get_x() + b.get_width()/2, b.get_height() + max(times)*0.02,
                    f'{t:.1f}ms', ha='center', va='bottom', fontsize=10)  # 막대 위에 응답 속도를 텍스트로 표시합니다.
        ax.set_title('IP Address Response Time', pad=18)  # 그래프 제목을 설정합니다.
        ax.set_ylabel('Response Time (ms)')  # y축의 라벨을 설정합니다.
        ax.set_xlabel('Provider')  # x축의 라벨을 설정합니다.
        ax.grid(True, axis='y', linestyle='--', alpha=0.3)  # y축에 점선 그리드를 표시합니다.
        plt.xticks(rotation=25, ha='right')  # x축의 라벨을 25도 회전시켜 덜 잘리게 합니다.
        ax.xaxis.labelpad = 6

    # constrained_layout로 기본 여백을 확보하고, 하단 여백을 더 넉넉히 설정합니다.
    fig.subplots_adjust(top=0.93, bottom=0.24)  # X축 라벨 회전으로 인한 하단 여백 확대
    return FigureCanvas(fig)  # Matplotlib 그림 객체를 Qt 위젯으로 변환하여 반환합니다.