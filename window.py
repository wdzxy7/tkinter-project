import tkinter as tk
import tkinter.messagebox
import os
import pymysql
import calculator
import game1
import game3
import hupu

connect = pymysql.connect(host='localhost', port=3306, user='root', passwd='', db='', charset='utf8')
cursor = connect.cursor()


# 计算器功能
def cal(window):
    window.destroy()
    calculator.calculator()
    creat()


# 游戏1
def plane(window):
    window.destroy()
    try:
        game1.main()
    finally:
        creat()


# 游戏2
def words(win):
    win.destroy()
    try:
        game3.main()
    finally:
        creat()


# 爬虫代码
def crawl(win):
    tkinter.messagebox.showinfo('提示', '开始爬虫')
    hupu.main()
    # time.sleep(10)
    if os.path.isfile("hupu.xlsx"):
        result = tkinter.messagebox.askokcancel('Message', '爬虫完成是否查看文件路径')
        if result is True:
            print(os.path.abspath("hupu.xlsx"))
            path = os.path.abspath("hupu.xlsx")
            tkinter.messagebox.showinfo('文件路径', path)


# 个人简历填写
def message(win):
    win.destroy()
    try:
        creat_message_box()
    finally:
        creat()


# 个人简历的创建，上面那个是调用
def creat_message_box():
    window = tk.Tk()
    window.title('个人简历')
    window.geometry('600x300')
    lable1 = tk.Label(window, text='姓名', fg="green", font=("华文行楷", 12), width=5, height=1)
    name = tk.Text(window, height=1)
    lable1.grid(row=0, column=0)
    name.grid(row=0, column=1)
    lable2 = tk.Label(window, text='名族', fg="green", font=('华文行楷', 12), width=5, height=1)
    nation = tk.Text(window, height=1)
    lable2.grid(row=1, column=0)
    nation.grid(row=1, column=1)
    lable3 = tk.Label(window, text='生日', fg="green", font=('华文行楷', 12), width=5, height=1)
    age = tk.Text(window, height=1)
    lable3.grid(row=3, column=0)
    age.grid(row=3, column=1)
    lable4 = tk.Label(window, text='电话', fg="green", font=('华文行楷', 12), width=10, height=1)
    telephone = tk.Text(window, height=1)
    lable4.grid(row=4, column=0)
    telephone.grid(row=4, column=1)
    lable5 = tk.Label(window, text='邮件', fg="green", font=('华文行楷', 12), width=10, height=1)
    email = tk.Text(window, height=1)
    lable5.grid(row=5, column=0)
    email.grid(row=5, column=1)
    lable6 = tk.Label(window, text='住址', fg="green", font=('华文行楷', 12), width=10, height=1)
    address = tk.Text(window, height=1)
    lable6.grid(row=6, column=0)
    address.grid(row=6, column=1)
    lable7 = tk.Label(window, text='学历', fg="green", font=('华文行楷', 12), width=10, height=1)
    education = tk.Text(window, height=1)
    lable7.grid(row=7, column=0)
    education.grid(row=7, column=1)
    lable8 = tk.Label(window, text='实习经历', fg="green", font=('华文行楷', 12), width=10, height=1)
    practice = tk.Text(window, height=1)
    lable8.grid(row=8, column=0)
    practice.grid(row=8, column=1)
    lable9 = tk.Label(window, text='获奖经历', fg="green", font=('华文行楷', 12), width=10, height=1)
    winning = tk.Text(window, height=1)
    lable9.grid(row=9, column=0)
    winning.grid(row=9, column=1)
    lable10 = tk.Label(window, text='自我评价', fg="green", font=('华文行楷', 12), width=10, height=1)
    self = tk.Text(window, height=1)
    lable10.grid(row=10, column=0)
    self.grid(row=10, column=1)
    button = tk.Button(window, text='提交', font=('Arial', 12), width=10, height=1, command=lambda: submit(name, nation, age, telephone, email, address, education, practice, winning, self))
    button.grid(row=12, column=1)
    button1 = tk.Button(window, text='查询', font=('Arial', 12), width=10, height=1, command=lambda: search(name, nation, age, telephone, email, address, education, practice, winning, self))
    button1.grid(row=13, column=1)


# 把填好的个人简历存到数据库
def submit(name, nation, age, telephone, email, address, education, practice, winning, self):
    global cursor
    name_message = name.get('0.0', 'end')
    nation_message = nation.get('0.0', 'end')
    age_message = age.get('0.0', 'end')
    telephone_message = telephone.get('0.0', 'end')
    email_message = email.get('0.0', 'end')
    address_message = address.get('0.0', 'end')
    education_message = education.get('0.0', 'end')
    practice_message = practice.get('0.0', 'end')
    winning_message = winning.get('0.0', 'end')
    self_message = self.get('0.0', 'end')
    sql = 'INSERT INTO test.temp (name, nation, age, telephone, email, address, education, practice, winning, self) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
    try:
        cursor.execute(sql, (name_message, nation_message, age_message, telephone_message, email_message, address_message, education_message, practice_message, winning_message, self_message))
        tkinter.messagebox.showinfo('提示', '写入成功')
    except Exception as e:
        print(str(e))


# 根据姓名查找某人的简历
def search(name, nation, age, telephone, email, address, education, practice, winning, self):
    window = tk.Tk()
    window.title('查询')
    window.geometry('500x300')
    lable1 = tk.Label(window, text='查询人姓名', fg="green", font=("华文行楷", 12), width=5, height=1)
    search_name = tk.Text(window, height=1)
    lable1.grid(row=0, column=0)
    search_name.grid(row=0, column=1)
    button = tk.Button(window, text='提交', font=('Arial', 12), width=10, height=1, command=lambda: write(window, search_name, name, nation, age, telephone, email, address, education, practice, winning, self))
    button.grid(row=1, column=1)


# 把上面函数查找的信息写入简历模板
def write(win, search_name, name, nation, age, telephone, email, address, education, practice, winning, self):
    global cursor
    sname = '\'' + str(search_name.get('0.0', 'end')) + '\''
    sql = 'select name, nation, age, telephone, email, address, education, practice, winning, self from test.temp where name = ' + sname + ';'
    try:
        cursor.execute(sql)
        result = cursor.fetchall()
    except:
        tkinter.messagebox.showinfo('提示', '没有此人')
        win.destroy()
        return None
    wname = str(result[0][0]).replace('(', '').replace(')', '').replace(',', '').replace(' ', '').replace('\n', '')
    wnation = str(result[0][1]).replace('(', '').replace(')', '').replace(',', '').replace(' ', '').replace('\n', '')
    wage = str(result[0][2]).replace('(', '').replace(')', '').replace(',', '').replace(' ', '').replace('\n', '')
    wtelephone = str(result[0][3]).replace('(', '').replace(')', '').replace(',', '').replace(' ', '').replace('\n', '')
    wemail = str(result[0][4]).replace('(', '').replace(')', '').replace(',', '').replace(' ', '').replace('\n', '')
    waddress = str(result[0][5]).replace('(', '').replace(')', '').replace(',', '').replace(' ', '').replace('\n', '')
    weducation = str(result[0][6]).replace('(', '').replace(')', '').replace(',', '').replace(' ', '').replace('\n', '')
    wpractice = str(result[0][7]).replace('(', '').replace(')', '').replace(',', '').replace(' ', '').replace('\n', '')
    wwinning = str(result[0][8]).replace('(', '').replace(')', '').replace(',', '').replace(' ', '').replace('\n', '')
    wself = str(result[0][9]).replace('(', '').replace(')', '').replace(',', '').replace(' ', '').replace('\n', '')
    name.delete('1.0', 'end')
    name.insert(tk.INSERT, wname)
    nation.delete('1.0', 'end')
    nation.insert(tk.INSERT, wnation)
    age.delete('1.0', 'end')
    age.insert(tk.INSERT, wage)
    telephone.delete('1.0', 'end')
    telephone.insert(tk.INSERT, wtelephone)
    email.delete('1.0', 'end')
    email.insert(tk.INSERT, wemail)
    address.delete('1.0', 'end')
    address.insert(tk.INSERT, waddress)
    education.delete('1.0', 'end')
    education.insert(tk.INSERT, weducation)
    practice.delete('1.0', 'end')
    practice.insert(tk.INSERT, wpractice)
    winning.delete('1.0', 'end')
    winning.insert(tk.INSERT, wwinning)
    self.delete('1.0', 'end')
    self.insert(tk.INSERT, wself)
    win.destroy()


def homework(str):
    name1 = str + 'homework.txt'
    name2 = str + 'analysis.txt'
    with open(name1,  encoding='UTF-8', mode='r') as f:
        home = f.read()
    with open(name2, encoding='UTF-8', mode='r') as f:
        ana = f.read()
    window = tk.Tk()
    window.title('作业')
    window.geometry('500x200')
    window2 = tk.Tk()
    window2.title('分析')
    # menus(window)
    example = tk.Text(window2, width=106, height=55)
    example.insert(tk.INSERT, ana)
    work = tk.Text(window, width=106, height=55)
    work.insert(tk.INSERT, home)
    example.pack()
    work.pack()
    button = tk.Button(window, text='提交', font=('Arial', 12), width=10, height=1, command=lambda: store_work(work, name1))
    button.pack()
    button = tk.Button(window2, text='提交', font=('Arial', 12), width=10, height=1,command=lambda: store_analysis(example, name2))
    button.pack()
    window.mainloop()
    window2.mainloop()


# 保存text写入的内容
def store_work(work, name):
    mes = work.get('0.0', 'end')
    with open(name,  encoding='UTF-8', mode='w') as f:
        f.write(mes)
    tkinter.messagebox.showinfo('提示', '请用python运行')


def store_analysis(example, name):
    mes = example.get('0.0', 'end')
    with open(name,  encoding='UTF-8', mode='w') as f:
        f.write(mes)
    tkinter.messagebox.showinfo('提示', '保存成功')


# 创建窗体
def creat():
    window = tk.Tk()
    window.title('My Window')
    window.geometry('500x300')
    menus(window)
    button1 = tk.Button(window, text='calculator', font=('Arial', 12), width=10, height=1, command=lambda: cal(window))
    button1.pack()
    button2 = tk.Button(window, text='game1', font=('Arial', 12), width=10, height=1, command=lambda: plane(window))
    button2.pack()
    button3 = tk.Button(window, text='game2', font=('Arial', 12), width=10, height=1, command=lambda: words(window))
    button3.pack()
    button4 = tk.Button(window, text='crawl', font=('Arial', 12), width=10, height=1, command=lambda: crawl(window))
    button4.pack()
    button5 = tk.Button(window, text='个人简历', font=('Arial', 12), width=10, height=1, command=lambda: message(window))
    button5.pack()
    button5 = tk.Button(window, text='作业', font=('Arial', 12), width=10, height=1, command=lambda: homework())
    button5.pack()
    window.mainloop()


# 创建主页面菜单
def menus(win):
    allmenu = tkinter.Menu(win)
    filemenu = tkinter.Menu(allmenu, tearoff=0)
    filemenu.add_command(label='计算器 code', command=show_calculator)
    filemenu.add_command(label='game1 code', command=show_game1)
    filemenu.add_command(label='game2 code', command=show_game2)
    filemenu.add_command(label='crawl code', command=show_crawl)
    filemenu.add_command(label='个人简历 code', command=show_self)
    filemenu.add_command(label='作业 code', command=show_homework)
    allmenu.add_cascade(label='查看(V)', menu=filemenu)

    helpmenu = tkinter.Menu(allmenu, tearoff=0)
    helpmenu.add_command(label='查看帮助', command=get_help)
    allmenu.add_cascade(label='帮助(H)', menu=helpmenu)

    win.config(menu=allmenu)


# 读取py txt文件显示代码
def show_calculator():
    window = tk.Tk()
    window.title('show_calculator')
    window.geometry('600x900')
    with open("calculator.py",  encoding='UTF-8') as f:
        code = f.read()
    code_information = tk.Text(window, width=200, height=500)
    code_information.insert(tk.INSERT, code)
    code_information.config(state=tk.DISABLED)
    button = tk.Button(window, text='分析+作业', font=('Arial', 12), width=10, height=1, command=lambda: homework('calculator'))
    button.pack(side=tk.TOP)
    code_information.pack(side=tk.BOTTOM)
    window.mainloop()


def show_game1():
    window = tk.Tk()
    window.title('show_calculator')
    window.geometry('600x900')
    with open("game1.py",  encoding='UTF-8') as f:
        code = f.read()
    code_information = tk.Text(window, width=400, height=500)
    code_information.insert(tk.INSERT, code)
    code_information.config(state=tk.DISABLED)
    button = tk.Button(window, text='分析+作业', font=('Arial', 12), width=10, height=1, command=lambda: homework('game1'))
    button.pack(side=tk.TOP)
    code_information.pack(side=tk.BOTTOM)
    window.mainloop()


def show_game2():
    window = tk.Tk()
    window.title('show_calculator')
    window.geometry('600x900')
    with open("game3.py",  encoding='UTF-8') as f:
        code = f.read()
    code_information = tk.Text(window, width=200, height=500)
    code_information.insert(tk.INSERT, code)
    code_information.config(state=tk.DISABLED)
    button = tk.Button(window, text='分析+作业', font=('Arial', 12), width=10, height=1, command=lambda: homework('game2'))
    button.pack(side=tk.TOP)
    code_information.pack(side=tk.BOTTOM)
    window.mainloop()


def show_crawl():
    window = tk.Tk()
    window.title('show_calculator')
    window.geometry('600x900')
    with open("hupu.py",  encoding='UTF-8') as f:
        code = f.read()
    code_information = tk.Text(window, width=200, height=500)
    code_information.insert(tk.INSERT, code)
    code_information.config(state=tk.DISABLED)
    button = tk.Button(window, text='分析+作业', font=('Arial', 12), width=10, height=1, command=lambda: homework('crawl'))
    button.pack(side=tk.TOP)
    code_information.pack(side=tk.BOTTOM)
    window.mainloop()


def show_self():
    window = tk.Tk()
    window.title('show_calculator')
    window.geometry('600x900')
    with open("resume_code.txt",  encoding='UTF-8') as f:
        code = f.read()
    code_information = tk.Text(window, width=200, height=500)
    code_information.insert(tk.INSERT, code)
    code_information.config(state=tk.DISABLED)
    button = tk.Button(window, text='分析+作业', font=('Arial', 12), width=10, height=1, command=lambda: homework('self'))
    button.pack(side=tk.TOP)
    code_information.pack(side=tk.BOTTOM)
    window.mainloop()


def show_homework():
    window = tk.Tk()
    window.title('show_homework')
    window.geometry('600x900')
    with open("work.txt", encoding='UTF-8') as f:
        code = f.read()
    code_information = tk.Text(window, width=200, height=500)
    code_information.insert(tk.INSERT, code)
    code_information.config(state=tk.DISABLED)
    button = tk.Button(window, text='分析+作业', font=('Arial', 12), width=10, height=1, command=lambda: homework('work'))
    button.pack(side=tk.TOP)
    code_information.pack(side=tk.BOTTOM)
    window.mainloop()


def get_help():
    tkinter.messagebox.showinfo('提示', '请使用python编写')


if __name__ == '__main__':
    creat()

