from tkinter import *
win = Tk()
win.geometry("400x200")
win.title("pack")

ent = Entry(win)
ent.pack()

btn = Button(win)
btn.config(text = "버튼")
def aa():
    btn.pack(side = ent.get())
btn.config(command = aa)
btn.pack()

btn2 = Button(win)
btn2.config(text = "temp")
btn2.pack()

win.mainloop()
