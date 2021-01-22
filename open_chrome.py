import tkinter as tk
import xlrd
import xlutils.copy

count = 1
i = 0
url_list = []
first_choice = ''
second_choice = ''
last_choice = ''


def get_url(sheet):
    result = []
    message_sum = sheet.nrows + 1
    for i in range(2, message_sum):
        name = sheet.cell_value(i - 1, 1)
        result.append(name)
    return result


def store(table, first_label, second_label, remarks):
    global count
    table.write(count, 10, first_label)
    table.write(count, 11, second_label)
    table.write(count, 12, remarks)
    count = count + 1


def next_url(driver):
    global i, url_list
    url = url_list[i]
    var.set('url:' + url)
    i = i + 1
    driver.get(url)


def change(event):
    global first_choice
    choice = left_lb.get(left_lb.curselection())
    first_choice = choice
    if choice == '赛事相关':
        right_var.set(('历史赛事集锦', '赛事集锦', '比赛前瞻', '赛中事件讨论', '赛事复盘'))
    elif choice == '人员流动':
        right_var.set(('交易', '签约', '裁员', '流言'))
    elif choice == '球员':
        right_var.set(('单个球员水平讨论', '数据', '球员对比', '球员花边'))
    elif choice == '球队':
        right_var.set(('数据', '球队故事', '球队对比'))
    elif choice == '热点':
        right_var.set(('赛制规则', '奖项投票', '社会事件议论', '交易评价'))
    elif choice == '其他':
        right_var.set(('2K游戏', '科普', '篮球IP长文', '其他内容'))
    elif choice == '活动':
        right_var.set(('促活活动', '直播内容', '固定栏目', '商业合作'))
    elif choice == '无':
        right_var.set('无')


def update_excel(table):
    global first_choice, second_choice, last_choice
    if first_choice == '无':
        first_choice = ''
    if second_choice == '无':
        second_choice = ''
    if last_choice == '无':
        last_choice = ''
    print(first_choice, second_choice, last_choice)
    store(table, first_choice, second_choice, last_choice)


def get(event):
    global second_choice
    second_choice = right_lb.get(right_lb.curselection())


def get2(event):
    global last_choice
    last_choice = last_lb.get(last_lb.curselection())


def close_win(ws):
    ws.save('urls.xls')
    driver.close()
    window.destroy()


if __name__ == '__main__':
    path = 'urls.xls'
    data = xlrd.open_workbook(path)
    sheet = data.sheet_by_name("9.28篮球帖")
    # 获取url
    url_list = get_url(sheet)
    # 创建追加写入
    ws = xlutils.copy.copy(data)
    table = ws.get_sheet(1)
    # #####################     creat window     ####################################################
    window = tk.Tk()
    window.title('My Window')
    window.geometry('500x300')
    var = tk.StringVar()
    var.set('')
    label1 = tk.Label(window, textvariable=var, font=('Arial', 12), width=30, height=2)
    label1.grid(row=0, column=1)
    next_url_button = tk.Button(window, text="next_url", command=lambda: next_url(driver))
    next_url_button.grid(row=1, column=1)
    left_var = tk.StringVar()
    right_var = tk.StringVar()
    left_var.set(('赛事相关', '人员流动', '球员', '球队', '热点', '其他', '活动', '无'))
    right_var.set(' ')
    last_var = tk.StringVar()
    last_var.set(('无', '打不开', '与篮球无关'))
    left_lb = tk.Listbox(window, listvariable=left_var)
    right_lb = tk.Listbox(window, listvariable=right_var)
    last_lb = tk.Listbox(window, listvariable=last_var)
    left_lb.bind('<Double-Button-1>', change)
    right_lb.bind('<Double-Button-1>', get)
    last_lb.bind('<Double-Button-1>', get2)
    left_lb.grid(row=2, column=0)
    right_lb.grid(row=2, column=1)
    last_lb.grid(row=2, column=2)
    store_button = tk.Button(window, text="存储", command=lambda: update_excel(table))
    store_button.grid(row=3, column=1)
    close_button = tk.Button(window, text='关闭并储存', command=lambda: close_win(ws))
    close_button.grid(row=4, column=1)
    window.mainloop()

