from requests.exceptions import RequestException
import requests
from bs4 import BeautifulSoup
import re
from openpyxl import Workbook


store_num = 2


# 获取网页源码
def get_html(url):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.162 Safari/537.36'
        }
        response = requests.get(url, headers=headers)
        response.encoding = 'utf-8'
        if response.status_code == 200:
            return response.text
        return None
    except RequestException:
        return None


def detail_message(url):
    # 获取网页源码创建Beautifulsopu对象
    html = get_html(url)
    soup = BeautifulSoup(html, 'html.parser')
    # 获取节点
    div = soup.find_all('div', {'class': 'artical-main-content'})
    soup = BeautifulSoup(str(div), 'html.parser')
    p = soup.find_all('p')
    message = ''
    # 获取节点数据
    for i in p:
        for mes in i.stripped_strings:
            message = message + mes
    return message


# 存excle
def write(excle, title, message):
    global store_num
    key = 'A' + str(store_num)
    excle[key] = title
    key = 'B' + str(store_num)
    excle[key] = message
    store_num = store_num + 1


def main():
    # 开启excle
    wb = Workbook()
    excle = wb.active
    excle['A1'] = '标题'
    excle['B1'] = '详细内容'
    for page in range(1, 8):
        # 构建url
        url = 'https://voice.hupu.com/soccer/' + str(page)
        html = get_html(url)
        soup = BeautifulSoup(html, "html.parser")
        li = soup.find_all('div', {'class': 'news-list'})
        new_soup = BeautifulSoup(str(li), 'html.parser')
        a = new_soup.find_all('a')
        count = 0
        title_list = []
        # 整理获得得信息
        for i in a:
            count = count + 1
            url = i.get('href')
            pattern = r'https://voice'
            if re.match(pattern, url):
                message_url = url
            for message in i.stripped_strings:
                if count == 1:
                    tup = (message, message_url)
                    title_list.append(tup)
                if count == 4:
                    count = 0
        # 数据写入excle
        for num in range(len(title_list)):
            url = title_list[num][1]
            title = title_list[num][0]
            print(url, type(title))
            detail = detail_message(url)
            print(detail)
            write(excle, title, detail)
    wb.save("hupu.xlsx")


if __name__ == '__main__':
    main()
