from tkinter import *
from tkinter.ttk import *

win = Tk()
win.geometry("500x500+950+0")
win.option_add("*Font", "Arial 20")

# ListBox
# lb = Listbox(win)
# lb.config(selectmode="multiple") # 다중선택 옵션
# lb.insert(0, "1번")
# lb.insert(1, "2번")
# lb.insert(2, "3번")
# lb.insert(3, "4번")
# lb.pack()

# # CheckButton
# cv = IntVar()
# cb = Checkbutton(win, text = "1번", variable=cv)
# cb.pack()

# # RadioButton
# rv = IntVar()
# rb1 = Radiobutton(win, text = "1번", value = 0, variable = rv)
# rb2 = Radiobutton(win, text = "2번", value = 1, variable = rv)
# rb3 = Radiobutton(win, text = "3번", value = 3, variable = rv)
# rb1.pack()
# rb2.pack()
# rb3.pack()

# # Combobox
# cb_list = ["1", "2", "3"]
# cb = Combobox(win)
# cb.config(values = cb_list)
# cb.pack()

# # SpinBox
# sb = Spinbox(win)
# sb.config(from_=-1, to=1)
# sb.pack()

# Scale
scale = Scale(win)
scale = Scale(win, length=300, from_=0, to=50, orient="horizontal")
scale.pack()


# BUTTON
btn = Button(win)
btn.config(text = "옵션 선택")
def click():
    # text = lb.curselection()[0] #ListBox
    # text = cv.get() #CheckButton
    # lab_text = rv.get() # RadioButton
    # lab_text = cb.get() # ComboBox
    # lab_text = sb.get() # SpinBox
    lab_text = scale.get()
    lab.config(text = lab_text)
btn.config(command = click)
btn.pack()

# Label
lab = Label(win)
lab.pack()


win.mainloop()