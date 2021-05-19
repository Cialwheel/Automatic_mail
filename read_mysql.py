import pymysql
import pandas as pd
import numpy as np

#建立在24h中100个货币排名可变但货币不变，如果中途第100名货币和第101名交换位置等，该程序结果错误

coin_name = []
temp = []
price = []
diction = {}

def connect(): #连接mysql并获取24H价格变动
    db = pymysql.connect(host='localhost', user='root', password='123456', database='test01',charset='utf8')
    sqlcmd='SELECT 币种名称,价格_USD from api ORDER BY 币种名称 ASC'
    date = pd.read_sql(sqlcmd,db)
    for i in range(0, 2400, 24):
        coin_name.append(date['币种名称'][i])
        temp.clear()
        for j in range(i, i+24):
            temp.append(date['价格_USD'][j])
        difference = float(max(temp))-float(min(temp))
        price.append(difference)

def String(): #转成字典型排序
    for i in range(0,100):
        diction.update({coin_name[i]: price[i]})
    sort_dict = sorted(diction.items(), key=lambda x: x[1],reverse = True)
    for i in range (0,100):
        print(sort_dict[i][0])

if __name__ == '__main__':
    connect()
    String()





    '''  
  for i in range(0,500):
      id1 = [j for j, x in enumerate(coin_name) if x == coin_name[i]]
      temp.append(id1)
      print(temp)
      temp.clear()
      print(temp)
  print(price)
  '''