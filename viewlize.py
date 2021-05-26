import matplotlib
import requests
import schedule
import matplotlib.pyplot as plt
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.header import Header
import datetime
import json
import time
import chardet
import smtplib

volume = [] #当前交易量
quote = [] #当前涨跌幅
week_volume = [] #一周内每天的交易量
week_quote = [] #一周内每天的涨跌幅
month_volume = [] #一月内每天的交易量
month_quote = [] #一月内每天的涨跌幅
date = [] #每天的日期
datetemp = [] #每7天的日期

def get(): #获取当天最新数据，总交易量，涨跌幅
    try:
        url = 'https://data.block.cc/api/v3/price?slug=bitcoin&api_key=******************'
        req = requests.get(url=url).text
        json_req = json.loads(req)
        volume.append(json_req[0]['v'])
        quote.append(json_req[0]['c'])
        add_list()
        print('work')
    except Exception as e:
        print(e)
        time.sleep(60)
        schedule_time()

def add_list(): #加入当天交易量，涨跌幅。 形成一周，一月的数据列表
    #schedule.every().day.at("12.01").do(get())
    if (len(volume)>2):
        volume.remove(volume[0])
        quote.remove(quote[0])
    if (len(volume)==2):
        date.append(str(datetime.datetime.now().today().minute) + ',' + str(datetime.datetime.now().today().second))
        datetemp.append(str(datetime.datetime.now().today().minute) + ',' + str(datetime.datetime.now().today().second))
        week_volume.append(int(volume[1])-int(volume[0]))
        r_quote = round((quote[1]-quote[0])*100,5)
        week_quote.append(str(r_quote)+"%")
        month_volume.append(int(volume[1])-int(volume[0]))
        month_quote.append(str(r_quote)+"%")
    print(volume)
    print(week_quote)
    print(month_volume)
    print(date)
    view()

def schedule_time(): #定时爬取
    schedule.every(5).seconds.do(get)
    while True:
        schedule.run_pending()

def delete(): #清空列表中内容如果超过需求大小
    if (len(week_volume) >= 7):
        week_volume.clear()
        week_quote.clear()
        datetemp.clear()
    elif (len(month_volume) >= 30):
        month_volume.clear()
        month_quote.clear()
        date.clear()

def view(): #用已有数据线性图观测，并发到邮箱
    if (len(week_volume) == 7):
        temp_week = []
        for i in range(0,7):
            temp_week.append(datetemp[i])
        week_x = temp_week
        week_y_volume = week_volume
        plt.figure(figsize=(12, 4))
        plt.xlabel("(" + str(datetime.datetime.now().today().year) + ")" + 'current time')
        plt.ylabel('one day transaction volume')
        plt.title('Summary Changes In Transaction Volume For 7D')
        plt.plot(week_x,week_y_volume)
        plt.savefig('week_volume.pdf')
        plt.close()
        week_y_quote = week_quote
        plt.figure(figsize=(12, 4))
        plt.xlabel("(" + str(datetime.datetime.now().today().year) + ")" + 'current time')
        plt.ylabel('range of price up,down for one day')
        plt.title('Summary Changes In Range Of Price Up,Down For 7D')
        plt.plot(week_x,week_y_quote)
        plt.savefig('week_quote.pdf')
        String_email('一周7天涨跌幅,交易量变化汇总', '', 'week_quote.pdf','week_volume.pdf', '**********@163.com')
        delete()
    if (len(month_volume) == 30):
        month_x = date
        month_y_volume = month_volume
        plt.figure(figsize=(12, 4))
        plt.xlabel("(" + str(datetime.datetime.now().today().year) + ")" + 'current time')
        plt.ylabel('one day transaction volume')
        plt.title('Summary Of Changes In Transaction Volume For 30 Days')
        plt.plot(month_x,month_y_volume)
        plt.savefig('month_volume.pdf')
        plt.close()
        month_y_quote = month_quote
        plt.figure(figsize=(12, 4))
        plt.xlabel("(" + str(datetime.datetime.now().today().year) + ")" + 'current time')
        plt.ylabel('range of price up,down for one day')
        plt.title('Summary Of Changes In Range Of Price Up,Down For 30 Days')
        plt.plot(month_x,month_y_quote)
        plt.savefig('month_quote.pdf')
        String_email('一月30天涨跌幅，交易量变化汇总', '', 'month_quote.pdf', 'month_volume.pdf', '*********@163.com')
        delete()

def String_email(subject_content,body_content,file,file2,mail_receiver): #将邮件发到指定邮箱包括主题，内容及附件
    mail_host = "smtp.163.com"
    mail_sender = "****163.com"
    mail_license = "***********"
    mm = MIMEMultipart('related')
    mm["From"] = "**********@163.com"
    mm["to"] = "***********@163.com"
    mm["Subject"] = Header(subject_content, 'utf-8')
    message_text = MIMEText(body_content, "plain", "utf-8")
    mm.attach(message_text)
    image_data = open(file, 'rb')
    image_data2 = open(file2, 'rb')
    message_image = MIMEApplication(image_data.read())
    message_image2 = MIMEApplication(image_data2.read())
    message_image.add_header('Content-Disposition', 'attachment', filename=file)
    message_image2.add_header('Content-Disposition', 'attachment', filename=file2)
    image_data.close()
    image_data2.close()
    mm.attach(message_image)
    mm.attach(message_image2)
    stp = smtplib.SMTP()
    stp.connect(mail_host)
    stp.login(mail_sender, mail_license)
    stp.sendmail(mail_sender, mail_receiver, mm.as_string())
    stp.quit()

if __name__ == '__main__':
    schedule_time()
    #test()
