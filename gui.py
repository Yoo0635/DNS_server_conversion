# gui.py
import tkinter as tk
from tkinter import messagebox # 팝업 메시지를 위해 임포트
import threading # 백그라운드 작업을 위해 임포트
import time # 시뮬레이션용 시간 지연을 위해 임포트

import api_client # api_client.py에서 정의한 함수들을 사용하기 위해 임포트

class TicketApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("스마트 티켓팅 시스템 - 예매")
        self.root.geometry("600x400") # 창 크기 설정

        # --- UI 요소 생성 ---
        self.title_label = tk.Label(self.root, text="공연 예매", font=("Arial", 24))
        self.title_label.pack(pady=20)

        self.status_label = tk.Label(self.root, text="준비 완료", font=("Arial", 14), fg="blue")
        self.status_label.pack(pady=10)

        self.reserve_button = tk.Button(self.root, text="티켓 예매하기", command=self.start_reservation)
        self.reserve_button.pack(pady=20)

        self.queue_label = tk.Label(self.root, text="현재 대기열: - 명", font=("Arial", 12))
        self.queue_label.pack(pady=5)

        self.exit_button = tk.Button(self.root, text="종료", command=self.root.quit)
        self.exit_button.pack(pady=10)

        # 예매 진행 중인지 나타내는 플래그
        self.is_reserving = False

    def start_reservation(self):
        if self.is_reserving:
            messagebox.showwarning("경고", "이미 예매 진행 중입니다.")
            return

        self.is_reserving = True
        self.reserve_button.config(state=tk.DISABLED) # 버튼 비활성화
        self.status_label.config(text="예매 요청 중...", fg="orange")
        self.queue_label.config(text="현재 대기열: 확인 중...")

        # --- 백엔드 통신을 별도의 스레드에서 시작 ---
        # 이렇게 해야 UI가 멈추지 않습니다!
        threading.Thread(target=self._reserve_ticket_async).start()

    def _reserve_ticket_async(self):
        """
        예매 요청을 비동기적으로 처리하는 함수 (별도 스레드에서 실행)
        """
        try:
            # 1. 예매 요청 (api_client 호출)
            # api_client.py의 함수를 호출하여 백엔드와 통신합니다.
            response = api_client.request_reservation(user_id="test_user_123", ticket_count=1)

            # 2. 대기열 상태 업데이트 (시뮬레이션)
            for i in range(5, 0, -1): # 5초 동안 대기열 감소 시뮬레이션
                self.root.after(1000, lambda i=i: self.queue_label.config(text=f"현재 대기열: {i}명"))
                time.sleep(1) # 스레드에서 sleep하여 UI 멈춤 방지

            # 3. 응답 처리 및 UI 업데이트
            if response.get("status") == "success":
                message = response.get("message", "티켓 예매가 성공적으로 완료되었습니다!")
                self.status_label.config(text="예매 성공!", fg="green")
                messagebox.showinfo("성공", message)
            elif response.get("status") == "queue":
                queue_pos = response.get("queue_position", "대기 중")
                message = response.get("message", f"현재 대기열에 있습니다. 순서: {queue_pos}")
                self.status_label.config(text="대기열 진입", fg="blue")
                messagebox.showinfo("대기열", message)
            else:
                error_message = response.get("message", "티켓 예매에 실패했습니다.")
                self.status_label.config(text="예매 실패", fg="red")
                messagebox.showerror("오류", error_message)

        except Exception as e:
            self.status_label.config(text="오류 발생", fg="red")
            messagebox.showerror("예매 오류", f"예매 중 오류가 발생했습니다: {e}")
        finally:
            self.is_reserving = False
            self.reserve_button.config(state=tk.NORMAL) # 버튼 다시 활성화
            self.queue_label.config(text="현재 대기열: - 명")


    def run(self):
        self.root.mainloop()