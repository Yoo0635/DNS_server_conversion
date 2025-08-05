from tkinter import *
import random
from datetime import datetime
win = Tk()
win.geometry("600x300")
win.title("place")
win.title("AIM_GAME")
win.geometry("550x150")

xx = 0.3    # 상대크기면 창의크기가 1이므로 좌표는 (0~1사이)
yy = 0.4
# Label
lab = Label(win)
lab.config(text = "표적 개수")
lab.grid(column=0, row= 0, padx=20, pady=20)

# Entry
ent = Entry(win)
ent.grid(column=1, row=0, padx=20, pady=20)

k = 1

def cc():
    global k
    if k < num_t:
        k += 1
        btn.destroy()
        ran_btn()
    else:
        fin = datetime.now()
        dif_sec = (fin-start).total_seconds()
        btn.destroy()
        lab = Label(win)
        lab.config(text = "Clear " + str(dif_sec) + "초")
        lab.pack(pady = 230)

def ran_btn():
    global btn
    btn = Button(win)
    btn.config(bg = "red")
    btn.config(command = cc)
    btn.config(text = k)
    btn.place(relx= random.random(), rely = random.random())

def btn_f():
    global num_t
    global start
    num_t = int(ent.get())
    for wg in win.grid_slaves(): # [label, entry, button]
        wg.destroy()
    win.geometry("500x500")
    ran_btn()
    start = datetime.now()

# Button
btn = Button(win)
btn.config(text = "({},{})".format(xx,yy))
btn.place(relx=xx, rely=yy)     # relx 는 상대크기 (그냥 x는 절대크기:창크기에 상관없이 위치고정)
btn.config(text = "시작")
btn.config(command = btn_f)
btn.grid(column=0, row=1, columnspan=2)

win.mainloop()