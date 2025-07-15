from tkinter import *
from datetime import datetime

win = Tk()                    # 창 생성 시작
win.geometry("600x100")       # 창 크기 설정 (가로 600, 세로 100)
win.title("what time?")       # 창 제목 설정
win.option_add("*Font", "궁서 20")  # 전체 글꼴 설정

def what_time():              # 현재 시각 표시 함수 정의
    dnow = datetime.now()     # 현재 날짜와 시간 가져오기
    # datetime 객체를 문자열로 변환하여 버튼 텍스트로 설정
    btn.config(text=dnow.strftime("%Y-%m-%d %H:%M:%S"))

btn = Button(win)             # 버튼 생성
btn.config(text="현재 시각")  # 버튼에 표시할 초기 텍스트 설정
btn.config(width=30)          # 버튼 너비 설정
btn.config(command=what_time) # 버튼 클릭 시 what_time 함수 실행

btn.pack()                   # 버튼을 창에 배치

win.mainloop()               # 이벤트 루프 시작, 창이 닫힐 때까지 실행 유지
