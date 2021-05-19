import datetime
import requests
import pymysql
from operator import itemgetter
from apscheduler.schedulers.blocking import BlockingScheduler
import json

#创建list
coin_name = list()
market_cap = list()
market_volume = list()
rmarket_volume = list()
price = list()
market_circulation = list()
quote_change = list()
week_quote = list()

def Api_key(): #寻找数据
    url1 = 'https://data.block.cc/api/v3/price?api_key=NRL9HC7ZSIWQU4JKMFPGUIZJMZFTWAXNH38SSVL1&size=100'       #货币名，市值，交易量，价格，24H涨跌幅，7D涨跌幅
    url2 = 'https://data.block.cc/api/v3/symbols/?api_key=NRL9HC7ZSIWQU4JKMFPGUIZJMZFTWAXNH38SSVL1&size=100'        #流通量
    response = requests.get(url1).text
    response2 = requests.get(url2).text
    r = json.loads(response)
    r2 = json.loads(response2)
    sortr = sorted(r, key=itemgetter('m'),reverse=True)             #按市值排序
    sortr2 = sorted(r2, key=itemgetter("marketCapUsd"),reverse=True)
    for i in range(0,100):      #各项加入list
        coin_name.append(sortr2[i]['symbol'])
        market_cap.append(sortr[i]['m'])
        market_volume.append(sortr[i]['v'])
        rmarket_volume.append(sortr[i]['rv'])
        price.append(sortr[i]['u'])
        market_circulation.append(sortr2[i]['availableSupply'])
        quote_change.append(sortr[i]['c'])
        week_quote.append(sortr[i]['cw'])

def String(): #存入数据
    #for i in range(0,100):
        #print({"币种名称":coin_name[i]},{"市值(USD)":market_cap[i]},{"交易量(USD)":market_volume[i]},
              #{"报告交易量(USD)":rmarket_volume[i]},{"价格(USD)":price[i]},{"流通量":market_circulation[i]},
              #{"24H涨跌幅":quote_change[i]},{"7D涨跌幅":week_quote[i]})
    db = pymysql.connect(host='localhost', user='root', password='123456', database='test01',charset='utf8')
    cursor = db.cursor()
    cursor.execute("delete from api")
    for i in range(0,100):
        sql = "INSERT INTO api VALUES('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s',now())"
        data = (coin_name[i],market_cap[i],market_volume[i],rmarket_volume[i],price[i],market_circulation[i],str(quote_change[i]*100)+"%",str(week_quote[i]*100)+"%")
        cursor.execute(sql % data)
        db.commit()
    db.close()

def set_time(): #开启定时
    sched = BlockingScheduler()
    sched.add_job(String, 'interval', minutes=1, id='test')
    sched.start()

def end_time(): #关闭定时
    sched = BlockingScheduler()
    sched.add_job(String, 'interval', hours=1, id='test')
    sched.remove_job(job_id='test')

if __name__ == '__main__':
    #Api_key()
    #String()
    end_time()
