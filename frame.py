from tkinter import *
from tkinter.filedialog import *
import csv
import requests

title = ''


def Crawl():#放爬虫代码
    global entry, title, text
    url = entry.get()
    if url == 'http://www.chengyudaquan.net/12shengxiaodechengyu/list_page.html':
        page_num = 9  # 共有9页
        title = '生肖'  # 名字，用于生成txt
        run([url, page_num, title])  # 传入url等参数  到爬虫函数
    elif url == 'http://www.chengyudaquan.net/miaoxiejijiedechengyu/list_page.html':
        page_num = 1
        title = '季节'
        run([url, page_num, title])
    elif url == 'http://www.chengyudaquan.net/chengyuzhongdeyanse/list_page.html':
        page_num = 2
        title = '心情'
        run([url, page_num, title])
    elif url == 'http://www.chengyudaquan.net/chengyuzhongdeyanse/list_page.html':
        page_num = 2
        title = '颜色'
        run([url, page_num, title])
    filename = title + '.txt'
    with open(filename, 'r+', encoding='utf-8') as f:
        message = f.read()
    text.insert("end", message)


def Save1():
    filename = asksaveasfilename(title = '另存为',initialfile = '未命名.txt',filetype = [('文本文档','*.txt')])
    fn = open(filename,'w')
    fn.write(text.get())
    fn.close()


def Save2():
    print ('hello')


def run(item):#每个板块把各自参数传到这个函数 这个函数爬取信息
    words=''
    url,page_num,title=item#分别获得参数列表里的参数
    page_num=int(page_num)#页码变为整形
    for p in range(1,page_num+1):#历遍每一页
        pageurl=url.replace('page',str(p))#把当前爬取的页码放入url中 构成完整url
        res = requests.get(pageurl)  # 访问url
        res.encoding = 'gbk'  # 改变中文编码
        html = res.text  # 获取源码
        result = re.findall('"mainlia1 wzbtlist"><a title="(.*?)"', html)  # 用正则获取页面中所有成语
        for word in result:  # 筛选出四字成语
            if len(word) == 4:  # 长度为4
                words = words + word + '\n'  # 筛选出四字程序存入words字符串
    print(words)#将成语在界面显示出来
    with open(title+'.txt','w',encoding='utf8') as f:
        f.write(words)#将程序存入文件
        f.close()


root = Tk()
root.title('python爬虫') #标题
root.geometry("600x270+400+100") #设置界面大小与出现位置

me = Menu()
root.config(menu = me) #一级菜单
filemenu = Menu(me)
filemenu.add_command(label = '保存为TXT',accelerator = 'Crtl + Z',command =  Save1)
filemenu.add_command(label = '保存为SQL',accelerator = 'Crtl + C',command =  Save2)#三级菜单
me.add_cascade(label = '文件',menu = filemenu) # 二级菜单

label = Label(root,text  = '输入要爬取的网址:',font = ('微软雅黑',15))#控件
label.grid() #选择文本输出位置

entry = Entry(root, width = 50)
entry.grid(row = 0,column = 1)#设置搜索框的位置

text = Text(root,width = 80,height=15)
text.grid(row=1,columnspan=2,sticky = W)#合并两列

button = Button(root,text = '开始爬取',command = Crawl)
button.grid(row = 2,column = 0,sticky = W)#定义爬取按钮

button1 = Button(root,text = '退出',command = root.quit)
button1.grid(row = 2,column = 1,sticky = E)#定义推出按钮

root.mainloop()