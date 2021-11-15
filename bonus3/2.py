# M11007309 鄭維新
# 該程式使用爬蟲將主力買賣超的資料抓取下來，並且提供使用者輸入任一股票代號，如輸入錯誤會跳出查無此股票代號

from bs4 import BeautifulSoup
import requests
import numpy as np
import pandas as pd
from tabulate import tabulate

# 個股主力和價格
print("input stock number")
stock_number = input()

check = requests.get(
    "https://tw.stock.yahoo.com/quote/" + stock_number + "/news")
if(check.ok):
    response = requests.get("http://jsjustweb.jihsun.com.tw/z/zc/zco/zco_"+stock_number+".djhtm")
else:
    print("查無此股票代號")

soup = BeautifulSoup(response.content, "html.parser")
firms = soup.find_all('td',{'class':'t4t1'})
datas = soup.find_all('td', {'class': 't3n1'})
dd = soup.find_all('div', {'class': 't11'})

date = dd[0].getText()[11:]
date = date.replace("/", "_")

buy = {}
sale = {}
for x in range(1,int(len(firms)/2-1)):
    buy[x] = []
    sale[x] = []

i = 1
j = 1
for x in firms:
    firm = x.getText()
    if( j %2 == 1 ):
        buy[i].append(firm)
        j+=1
    else:
        sale[i].append(firm)
        j+=1
        i+=1
    if(i == len(firms)/2-1):
        break

i = 0
j = 1
for x in datas:
    data = x.getText()
    i+=1
    if(i <= 4):
        buy[j].append(data)
    else:
        sale[j].append(data)
    if(i == 8):
        i = 0
        j+=1
    if(j == 16):
        break

buy_df = pd.DataFrame.from_dict(
    buy, orient='index', columns=['買超券商', '買進', '賣出', '買超', '佔交易比重'])
sale_df = pd.DataFrame.from_dict(
    sale, orient='index', columns=['賣超券商', '買進', '賣出', '賣超' , '佔交易比重'])

print(date+"\n"+stock_number+"主力進出明細")
buy_df.to_csv(date+"買超券商.csv", encoding='big5')
sale_df.to_csv(date+"賣超券商.csv", encoding='big5')

print("主力買超")
print(tabulate(buy_df,headers='keys',tablefmt='psql'))
print("主力賣超")
print(tabulate(sale_df,headers='keys',tablefmt='psql'))