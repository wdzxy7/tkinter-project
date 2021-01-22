import tkinter as tk
import pymysql

connect = pymysql.connect(host='localhost', port=3308, user='root', passwd='', db='db_test', charset='utf8')
cursor = connect.cursor()
exe_sql = ''


def execute_sql(sql):
    global cursor
    cursor.execute(sql)
    result = cursor.fetchall()
    string = ''
    for i in result:
        string = string + str(i) + '\n'
    string = string.replace('(', '').replace(')', '').replace('\'', '')
    work.delete('1.0', 'end')
    work.insert(tk.INSERT, string)


def chose(event):
    global exe_sql
    ch = choice.get(choice.curselection())
    if ch != 'sql11':
        exe_sql = sqls[ch]
        print(exe_sql)
        var_l.set(exe_sql)
    else:
        temp = tk.Tk()
        l1 = tk.Label(temp, text="请输入分数下限")
        l1.pack()
        text1 = tk.StringVar()
        low = tk.Entry(temp, textvariable=text1)
        text1.set(" ")
        low.pack()

        l2 = tk.Label(temp, text="请输入分数上限")
        l2.pack()
        text1 = tk.StringVar()
        high = tk.Entry(temp, textvariable=text1)
        text1.set(" ")
        high.pack()

        tk.Button(temp, text="点击确认", command=lambda: on_click(temp, low, high)).pack()
        temp.mainloop()


def on_click(temp, entry1, entry2):
    global exe_sql
    low = entry1.get()
    high = entry2.get()
    exe_sql = 'CALL work(' + str(low) + ', ' + str(high) + ');'
    var_l.set(exe_sql)
    temp.destroy()


if __name__ == '__main__':
    window = tk.Tk()
    window.title('欢迎')
    window.geometry('800x600')
    sqls = {'sql1': 'select SNO, SNAME, (2019 - SAGE) FROM db_test.student;',
            'sql2': 'SELECT SDEPT, COUNT(SNO) FROM db_test.student GROUP BY SDEPT desc;',
            'sql3': 'SELECT DISTINCT A.SNO, CNO, GRADES FROM db_test.score AS A, db_test.student AS B '
                'WHERE (CNO=\'2\' OR CNO=\'3\');',
            'sql4': 'SELECT TNAME, COUNT(score.CNO) FROM db_test.teacher, db_test.score WHERE score.CNO = teacher.CNO '
                'GROUP BY TNAME HAVING COUNT(score.CNO) > 3;',
            'sql5': 'SELECT DISTINCT SNAME, SDEPT FROM db_test.student, db_test.score WHERE student.SNO '
                'NOT IN (SELECT score.SNO FROM db_test.score);',
            'sql6': 'SELECT MAX(GRADES),CNO FROM db_test.score, db_test.student WHERE score.SNO=student.SNO GROUP BY CNO;',
            'sql7': 'SELECT DISTINCT TNAME FROM db_test.teacher, db_test.course WHERE CNAME=\'数据结构\' '
                'AND course.CNO=teacher.CNO;',
            'sql8': 'SELECT ST.SNO, SNAME, SSEX, SAGE, SDEPT FROM '
                'db_test.student AS ST, db_test.score AS SC, db_test.course AS CO, db_test.teacher AS TE '
                'WHERE TNAME = \'李正科\' AND SC.SNO=ST.SNO AND SC.CNO=TE.CNO AND SC.CNO=CO.CNO;',
            'sql9': 'SELECT * FROM db_test.s1;',
            'sql10': 'SELECT * FROM db_test.view;'
            }
    var = tk.StringVar()
    var.set(('sql1', 'sql2', 'sql3', 'sql4', 'sql5', 'sql6', 'sql7', 'sql8', 'sql9', 'sql10', 'sql11'))
    choice = tk.Listbox(window, listvariable=var)
    var_l = tk.StringVar()
    var_l.set('')
    label1 = tk.Label(window, textvariable=var_l, font=('Arial', 12), width=160, height=2)
    label1.grid(row=0, column=0)
    work = tk.Text(window, width=106, height=40)
    work.grid(row=3, column=0)
    bt_login = tk.Button(window, text='Execute Sql', command=lambda: execute_sql(exe_sql))
    choice.grid(row=2, column=0)
    choice.bind('<Double-Button-1>', chose)
    bt_login.grid(row=1, column=0)
    window.mainloop()