import requests, re


def sx():#生肖  #四个板块的爬虫函数入口
    url='http://www.chengyudaquan.net/12shengxiaodechengyu/list_page.html'#生肖页面url  ‘page’后面或会换成相应的页码 比如list_1 代表第一页
    page_num=9#共有9页
    title='生肖'#名字，用于生成txt
    run([url, page_num, title])# 传入url等参数  到爬虫函数


def jj():#季节
    url='http://www.chengyudaquan.net/miaoxiejijiedechengyu/list_page.html'
    page_num = 1
    title = '季节'
    run([url,page_num,title])


def xq():#心情
    url='http://www.chengyudaquan.net/chengyuzhongdeyanse/list_page.html'
    page_num = 2
    title = '心情'
    run([url, page_num, title])


def ys():#颜色
    url='http://www.chengyudaquan.net/chengyuzhongdeyanse/list_page.html'
    page_num = 2
    title = '颜色'
    run([url, page_num, title])


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


if __name__ == '__main__':#程序从这里开始运行
    sx()#生肖 调用四个板块的函数
    jj() # 季节
    xq()#心情
    ys()# 颜色