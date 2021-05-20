import pymysql
import pandas as pd
from collections import defaultdict

#创建普通字典，list和key可以存放多值的字典
coin_name = []
temp = defaultdict(list)
coin_difference = {}

def connect(): #建立连接存入所有值
    db = pymysql.connect(host='localhost', user='root', password='123456', database='test01',charset='utf8')
    sqlcmd = 'SELECT 币种名称,价格_USD from api ORDER BY 币种名称 ASC'
    date = pd.read_sql(sqlcmd,db)
    for i in range(0,500):
        temp[date['币种名称'][i]].append(date['价格_USD'][i])
        price = temp.get(date['币种名称'][i])
        if len(price) > 1: #如果中途后100名货币跑到前100来，而其中被替代的货币只出现过一次，那么不把它算入24h内价格变动
            difference = float(max(price))-float(min(price))
            coin_difference[date['币种名称'][i]] = difference
        else:
            continue

def String(): #进行排序打印
    sort_dict = sorted(coin_difference.items(), key=lambda x: x[1], reverse=True)
    for i in range(0,len(sort_dict)):
        print(sort_dict[i][0])

if __name__ == '__main__':
    connect()
    String()


