# main.py
import gui

if __name__ == "__main__":
    app = gui.TicketApp() # gui.py에서 정의한 TicketApp 클래스 인스턴스 생성
    app.run() # 앱 실행