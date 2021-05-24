from web3 import Web3,HTTPProvider, IPCProvider
from web3.eth import Eth
import schedule
import pymysql
import hex

value_from = []
value_to = []
value_miner = []

'''
def web():
    for i in range(0,block.number):
        get_block(i)
'''

def get_block(): #获取当前最新区块中的交易信息（1，发起者的余额 2，接受者的余额 3，挖矿者的余额）
    new_block = w3.eth.getBlock('latest')
    for i in range(0,len(new_block.transactions)):
        transaction = new_block.transactions[i].hex()
        transaction_info = w3.eth.getTransaction(str(transaction))
        temp_from = w3.eth.getBalance(transaction_info.get('from'))/10**18
        temp_to = w3.eth.getBalance(transaction_info.to)/10**18
        temp_miner = w3.eth.getBalance(new_block.miner)/10**18
        value_from.append(round(temp_from,3))
        value_to.append(round(temp_to,3))
        value_miner.append(round(temp_miner,3))
    count = len(new_block.transactions)
    return count

def String():
    length = get_block()
    db = pymysql.connect(host='localhost', user='root', password='***', database='test01', charset='utf8')
    cursor = db.cursor()
    for i in range(0,length):
        sql = "INSERT INTO block VALUES('%s', '%s', '%s')"
        date = (str(value_from[i])+"Eth",str(value_to[i])+"Eth",str(value_miner[i])+"Eth")
        cursor.execute(sql % date)
        print("good")
        db.commit()
    db.close()

def test(): #测试使用
    transaction_info = w3.eth.getTransaction(block.transactions[0].hex())
    #print(transaction_info.get('from')
    c = [12.212121,12.3243243,13.213213,15.213213]
    for i in range(0,int(49/10)):
        print(round(c[i],2))


if __name__ == '__main__':
    w3 = Web3(Web3.HTTPProvider('https://mainnet.infura.io/v3/d4b28ab481044de7aa471d2a7a1a9dba'))
    block = w3.eth.get_block('latest')
    String()
    #test()