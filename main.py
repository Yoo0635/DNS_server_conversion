from tkinter import *
win = Tk()
win.title("Daum Log-in")
win.geometry("400x300")
# win.option("*Font", "궁서 20")

# 다음 로고
lab_d = Label(win)
img = PhotoImage(file = "/Users/ganghungi/Desktop/Daum.png", master = win)
img = img.subsample(2)
lab_d.config(image = img)
lab_d.pack()

# id 라벨
lab1 = Label(win)
lab1.config(text = "ID")
lab1.pack()

# id 입력창
ent1 = Entry(win)
ent1.insert(0, "temp@temp.com")
def clear(event):
    if ent1.get() == "temp@temp.com":
        ent1.delete(0, len(ent1.get()))
ent1.bind("<Button-1>", clear)
ent1.pack()

# pw 라벨
lab2 = Label(win)
lab2.config(text = "Password")
lab2.pack()

# pw 입력창
ent2 = Entry(win)
ent2.config(show = "*")
ent2.pack()

# 로그인 버튼
btn = Button(win)
btn.config(text = "로그인")

def login():
    xpath1 = "//input[@name= 'email']"      #개발자 모드에서 id 입력창 섹션을 찾는다
    driver.find_element_by_xpath(xpath1).send_keys(ent1.get())
    driver.implicitly_wait(5)
    xpath2 = "//input[@name='password']"
    driver.find_element_by_xpath(xpath2).send_keys(ent2.get())
    driver.implicitly_wait(5)
    xpath3 = "//button[@class='btn_g btn_confirm submit]"
    driver.find_element_by_xpath(xpath3).click()
    lab3.config(text = "[메세지] 로그인 성공!")

btn.config(command = login)
btn.pack()

# 메세지 라벨
lab3 = Label(win)
lab3.pack()

from selenium import webdriver
driver = webdriver.Chrom("@크롬웹드라이버 저장 경로")
url = "@다음홈페이지 로그인창 주소창" 
driver.get(url)
driver.implicitly_wait(5) #대기시간 5초





win.mainloop()