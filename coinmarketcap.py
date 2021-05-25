import requests
import json
import time
import logging
import datetime

market = []
title = []
content_url = []
times = []

def get(): #获取交易所名称，标题，内容以及时间
    url = 'https://data.block.cc/api/v3/announcements?locale=zh_CN&api_key=NRL9HC7ZSIWQU4JKMFPGUIZJMZFTWAXNH38SSVL1&size=100'
    req = requests.get(url=url).text
    json_req = json.loads(req)
    for i in range(0,100):
        market.append(json_req[i]['market'])
        title.append(json_req[i]['title'])
        content_url.append(json_req[i]['url'])
        timestamp = int(json_req[i]['timestamp'])
        times.append(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(timestamp / 1000)))
    String()

def String():
    for i in range(0,100):
        print('market:  '+str(market[i])+',','title:  '+str(title[i])+',', 'content_url:  '+str(content_url[i])+',', 'time:  '+str(times[i]))


if __name__ == '__main__':
    get()
    #test()