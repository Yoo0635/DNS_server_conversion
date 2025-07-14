from tkinter import *
win = TK() # 창 생성

win.geometry("1000 x 500")
win.title("temp")
win.option_add("*Font", "맑은고딕 25")

btn = Button(win, text = "버튼")

win.mainloop() # 창 실행