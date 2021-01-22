from pandas import DataFrame
import re

if __name__ == '__main__':
    store_list = []
    mess = ''
    with open('test.txt', 'r') as f:
        for line in f:
            if line == '\n':
                continue
            if re.findall(r'(January|February|March|April|May|July|June|August|September|Octover|November|December)', line) and len(line) < 20:
                day_time = line.replace('\n', '')
                for i in range(6):
                    line = f.readline()
            if line.startswith('Document'):
                mess = mess.lower().replace('to', '').replace('for', '').replace('.', '').\
                                    replace(',', '').replace('\n', '')
                tup = (day_time, mess)
                store_list.append(tup)
                mess = ''
                continue
            mess = mess + line
    dic = {}
    df = DataFrame(store_list)
    print(df)