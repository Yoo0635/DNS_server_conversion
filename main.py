from tkinter import *
win = Tk()
win.geometry("600x300")
win.title("place")

xx = 0.3    # 상대크기면 창의크기가 1이므로 좌표는 (0~1사이)
yy = 0.4

btn = Button(win)
btn.config(text = "({},{})".format(xx,yy))
btn.place(relx=xx, rely=yy)     # relx 는 상대크기 (그냥 x는 절대크기:창크기에 상관없이 위치고정)

win.mainloop()