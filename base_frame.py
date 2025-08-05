import tkinter as tk

class BaseFrame(tk.Frame):
    def __init__(self, master, switch_frame_callback, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.switch_frame_callback = switch_frame_callback

        back_btn = tk.Button(self, text="← 뒤로가기", 
                             command=self.go_back,
                             bg="#4c566a", fg="white", font=("Arial", 10, "bold"),
                             relief="flat", activebackground="#434c5e", activeforeground="white")
        back_btn.pack(side="top", anchor="w", padx=10, pady=10)

    def go_back(self):
        print("뒤로가기 버튼 눌림")
        self.on_destroy()
        # 약간 딜레이를 줘서 이벤트 루프 안정화
        self.after(10, lambda: self.switch_frame_callback("dashboard"))

    def on_destroy(self):
        """서브 클래스에서 예약된 작업 취소 등 정리작업을 위해 오버라이드"""
        pass
