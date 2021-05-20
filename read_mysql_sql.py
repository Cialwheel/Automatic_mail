import pymysql
import pandas as pd

def connect():
    db = pymysql.connect(host='localhost', user='root', password='123456', database='test01', charset='utf8')
    sqlcmd = "select 币种名称, max(价格_USD),min(价格_USD),max(价格_USD)-min(价格_USD)as difference from api group by 币种名称 having max(价格_USD)<> 0 and min(价格_USD)<> 0 order by difference desc"
    date = pd.read_sql(sqlcmd, db)
    for i in range(0,len(date)):
        print(date['币种名称'][i])

if __name__ == '__main__':
    connect()
