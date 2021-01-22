import tkinter as tk
import tkinter.messagebox
import pymysql
import time
# import characterrecongnition


connect = pymysql.connect(host='localhost', port=3306, user='root', passwd='', db='test', charset='utf8')
cursor = connect.cursor()
# 建立图形识别对象
# iden = characterrecongnition.SortWin()


def search_people(serch):
    user = serch.get().replace(' ', '')
    global cursor
    sql = 'select * from test.log_in where user=' + user + ';'
    print(sql)
    cursor.execute(sql)
    result1 = cursor.fetchall()
    sql = 'select * from test.register where username=' + user + ';'
    cursor.execute(sql)
    result2 = cursor.fetchall()
    name = str(result2[0][0]).replace('(', '').replace(')', '').replace('\'', '').replace(',', '')
    user = str(result1[0][0]).replace('(', '').replace(')', '').replace('\'', '').replace(',', '')
    time = str(result1[0][1]).replace('(', '').replace(')', '').replace('\'', '').replace(',', '')
    result = str(result1[0][2]).replace('(', '').replace(')', '').replace('\'', '').replace(',', '')
    password = str(result2[0][2]).replace('(', '').replace(')', '').replace('\'', '').replace(',', '')
    adm = str(result2[0][3]).replace('(', '').replace(')', '').replace('\'', '').replace(',', '')
    if adm == '1':
        string = '姓名:' + name + ' 用户名:' + user + ' 密码:' + password + \
                 ' 是管理员 上次登陆时间:' + time + '上次识别结果:' + result
    else:
        string = '姓名:' + name + '\n用户名:' + user + '\n密码:' + password + \
                 '\n不是管理员\n上次登陆时间:' + time + '\n上次识别结果:' + result
    tk.messagebox.showinfo('查询结果', string)


def delect_people(delect):
    user = delect.get()
    global cursor
    sql = 'DELETE from test.register where username=%s'
    cursor.execute(sql, user)
    sql = 'DELETE from test.log_in where user=%s'
    cursor.execute(sql, user)
    tk.messagebox.showinfo('提示', '删除成功')


def creat_adm():
    window = tk.Toplevel()
    window.title('欢迎')
    window.geometry('450x300')

    canvas = tk.Canvas(window, height=300, width=500)
    imagefile = tk.PhotoImage(file='2.gif')
    canvas.create_image(0, 0, anchor='nw', image=imagefile)
    canvas.pack(side='top')

    tk.Label(window, text='查询用户').place(x=100, y=150)
    search = tk.StringVar()
    entry_usr_name = tk.Entry(window, textvariable=search)
    entry_usr_name.place(x=160, y=150)
    search_button = tk.Button(window, text='查询', command=lambda: search_people(entry_usr_name))
    search_button.place(x=350, y=150)

    tk.Label(window, text='删除用户').place(x=100, y=190)
    delect = tk.StringVar()
    entry_usr_pwd = tk.Entry(window, textvariable=delect)
    entry_usr_pwd.place(x=160, y=190)
    delect_button = tk.Button(window, text='删除', command=lambda: delect_people(entry_usr_pwd))
    delect_button.place(x=350, y=190)
    window.mainloop()


def creat_user(user):
    window = tk.Toplevel()
    window.title('欢迎')
    window.geometry('450x300')
    identify_button = tk.Button(window, text='文字识别', command=lambda: identify)
    save_button = tk.Button(window, text='保存结果', command=lambda: save(user))
    identify_button.place(x=100, y=150)
    save_button.place(x=100, y=190)


def identify():
    global iden
    iden.show()


def save(user):
    global cursor, iden
    t1 = str(time.localtime())
    path = iden.result
    if path == '':
        tk.messagebox.showerror('提示', 'n你还没有执行图形识别代码')
        return None
    with open(path, 'r') as f:
        txt = f.read()
    sql = 'select * from test.log_in where user=%s;'
    cursor.execute(sql, user)
    result = cursor.fetchall()
    if len(result) == 0:
        sql = 'INSERT INTO test.log_in (user, time, result) VALUES (%s, %s, %s)'
    else:
        sql = 'update test.log_in set user=%s, time=%s, result=%s where user = ' + user + ';'
    try:
        cursor.execute(sql, (user, t1, txt))
        tk.messagebox.showinfo('提示', '写入成功')
    except:
        tk.messagebox.showinfo('提示', '写入失败')


def usr_log_in(var_usr_name, var_usr_pwd):
    user = var_usr_name.get()
    password = var_usr_pwd.get()
    result = get_password(user)
    if len(result) == 0:
        tk.messagebox.showerror('错误', '没有此账号')
    elif str(result[0]).replace('\'', '').replace('(', '').replace(')', '').replace(',', '') != password:
        tk.messagebox.showerror('错误', '密码错误')
    else:
        result = admin(user)
        result = str(result[0]).replace('\'', '').replace('(', '').replace(')', '').replace(',', '')
        if result == '1':
            tk.messagebox.showinfo('提示', '管理员登陆成功')
            creat_adm()
        else:
            tk.messagebox.showinfo('提示', '普通用户登陆成功')
            creat_user(user)


def usr_sign_up():
    def signtowcg():
        # 获取输入框内的内容
        na = name.get()
        nn = new_name.get()
        np = new_pwd.get()
        npf = new_pwd_confirm.get()
        adm = whether.get()

        exist_usr_info = get_username(nn)
        print(exist_usr_info)

        # 检查用户名存在、密码为空、密码前后不一致
        if len(exist_usr_info) > 0:
            tk.messagebox.showerror('错误', '用户名已存在')
        elif np == '' or nn == '':
            tk.messagebox.showerror('错误', '用户名或密码为空')
        elif np != npf:
            tk.messagebox.showerror('错误', '密码前后不一致')
        # 注册信息没有问题则将用户名密码写入数据库
        else:
            write_message(na, nn, np, adm)
            tk.messagebox.showinfo('欢迎', '注册成功')
            # 注册成功关闭注册框
            window_sign_up.destroy()

    # 新建注册界面
    window_sign_up = tk.Toplevel(window)
    window_sign_up.geometry('350x200')
    window_sign_up.title('注册')
    # 姓名输入
    name = tk.StringVar()
    tk.Label(window_sign_up, text='姓名：').place(x=10, y=10)
    tk.Entry(window_sign_up, textvariable=name).place(x=150, y=10)
    # 用户名变量及标签、输入框
    new_name = tk.StringVar()
    tk.Label(window_sign_up, text='用户名：').place(x=10, y=50)
    tk.Entry(window_sign_up, textvariable=new_name).place(x=150, y=50)
    # 密码变量及标签、输入框
    new_pwd = tk.StringVar()
    tk.Label(window_sign_up, text='请输入密码：').place(x=10, y=90)
    tk.Entry(window_sign_up, textvariable=new_pwd, show='*').place(x=150, y=90)
    # 重复密码变量及标签、输入框
    new_pwd_confirm = tk.StringVar()
    tk.Label(window_sign_up, text='请再次输入密码：').place(x=10, y=130)
    tk.Entry(window_sign_up, textvariable=new_pwd_confirm, show='*').place(x=150, y=130)
    # 检查是否是管理员
    whether = tk.StringVar()
    tk.Label(window_sign_up, text='是否是管理员（是/否）：').place(x=10, y=170)
    tk.Entry(window_sign_up, textvariable=whether, show='*').place(x=150, y=170)
    # 确认注册按钮及位置
    bt_confirm_sign_up = tk.Button(window_sign_up, text='确认注册', command=signtowcg)
    bt_confirm_sign_up.place(x=150, y=210)


def get_username(num):
    global cursor
    sql = 'select username from test.register where username = %s'
    cursor.execute(sql, num)
    return cursor.fetchall()


def write_message(name, username, password, adm):
    if adm == '否':
        adm = 0
    else:
        adm = 1
    global cursor
    sql = 'INSERT INTO test.register (name, username, password, administrator) VALUES (%s, %s, %s, %s)'
    cursor.execute(sql, (name, username, password, adm))


def get_password(num):
    global cursor
    sql = 'select password from test.register where username =%s'
    cursor.execute(sql, num)
    return cursor.fetchall()


def admin(num):
    global cursor
    sql = 'select administrator from test.register where username =%s'
    cursor.execute(sql, num)
    return cursor.fetchall()


def usr_sign_quit():
    window.destroy()


if __name__ == '__main__':
    window = tk.Tk()
    window.title('欢迎')
    window.geometry('450x300')
    # 画布放置图片t

    canvas = tk.Canvas(window, height=300, width=500)
    imagefile = tk.PhotoImage(file='2.gif')
    canvas.create_image(0, 0, anchor='nw', image=imagefile)
    canvas.pack(side='top')

    # 标签 用户名密码
    tk.Label(window, text='用户名:').place(x=100, y=150)
    tk.Label(window, text='密码:').place(x=100, y=190)
    # 用户名输入框
    var_usr_name = tk.StringVar()
    entry_usr_name = tk.Entry(window, textvariable=var_usr_name)
    entry_usr_name.place(x=160, y=150)
    # 密码输入框
    var_usr_pwd = tk.StringVar()
    entry_usr_pwd = tk.Entry(window, textvariable=var_usr_pwd, show='*')
    entry_usr_pwd.place(x=160, y=190)
    bt_login = tk.Button(window, text='登录', command=lambda: usr_log_in(var_usr_name, var_usr_pwd))
    bt_login.place(x=140, y=230)
    bt_logup = tk.Button(window, text='注册', command=usr_sign_up)
    bt_logup.place(x=210, y=230)
    bt_logquit = tk.Button(window, text='退出', command=usr_sign_quit)
    bt_logquit.place(x=280, y=230)
    # 主循环
    window.mainloop()