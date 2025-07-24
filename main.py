from tkinter import *
win = Tk()
win.geometry("600x300")
win.title("pack")

# 4x3버튼 array 만들기
btn_list = []
col_num = 4
row_num = 3
for j in range(0, row_num):
    for i in range(0, col_num):
        btn = Button(win)
        btn.config(text = "({},{})".format(i,j))
        btn.grid(column = i, row = j, padx = 10, pady = 10)
        btn_list.append(btn)

btn = Button(win)
btn.config(text = "new")
btn.grid(column = 3, row = 0, rowspan = 2)      # 병합임. (3,0)좌표에서 row(세로)로 2칸 먹겠단뜻임
                                                # 그치만 아마 이쁘게 안뜰텐데 그냥 자신의 섹션만 먹는거임. 그래서 버튼크기를 키우던가해야지만 이쁘게 보일거임

'''
btn1 = Button(win)
btn1.config(text = "(0,0)")
btn1.grid(column = 0, row = 0)

btn2 = Button(win)
btn2.config(text = "(1,0)")
btn2.grid(column = 1, row = 0)

btn3 = Button(win)
btn3.config(text = "(0,1)")
btn3.grid(column = 0, row = 1)

btn4 = Button(win)
btn4.config(text = "(0,3)")
btn4.grid(column = 0, row = 3)      # grid 배치의 특징: 빈공간을 못만든다 ㅠ
'''


win.mainloop()