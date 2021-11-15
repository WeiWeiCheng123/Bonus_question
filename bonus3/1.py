# M11007309 鄭維新
# 該程式使用爬蟲將外資買賣超排行前20的資料抓取下來，而且可以讓使用者挑選上市上櫃以及天數

from bs4 import BeautifulSoup
import requests
import numpy as np
import pandas as pd
from tabulate import tabulate

# 外資買賣超排行

print("input category ( 上市：0 / 上櫃：1 )")
category = input()  # 上市(0)/上櫃(1)
print("input date ( 天數 : 1, 5, 10 )")
day = input()  # 天數 EX 1 5 10
print("input rank ( 排行數量 最大50筆 )")
rank = input()

response = requests.get(
    "http://fubon-ebrokerdj.fbs.com.tw/z/zg/zgk.djhtm?A=D&B="+category+"&C="+day)

soup = BeautifulSoup(response.content.decode('big5', 'ignore'), "html.parser")
stock_name = soup.find_all('td', {'class': 't3t1'}, limit=int(rank)*2)
stock_price = soup.find_all('td', {'class': 't3n1'}, limit=int(rank)*5)
dd = soup.find_all('div', {'class': 't11'})

for x in dd:
    date = x.getText()[3:]
date = date.replace("/", "_")

buy = {}
sale = {}
i = 0
for x in range(1,int(rank)+1):
    buy[x] = []
    sale[x] = []

i = 0
j = 1
for x in stock_name:
    name = x.getText()
    if(i % 2 == 0):
        buy[j].append(name)
    else:
        sale[j].append(name)
        j += 1
    i += 1

i = 0
j = 1
for x in stock_price:
    price = x.getText()
    if(price != "0"):
        if(i <= 1):
            buy[j].append(price)
        else:
            sale[j].append(price)
        if(i == 3):
            j += 1
            i = 0
        else:
            i += 1
    if(j == int(rank)+1):
        break

buy_df = pd.DataFrame.from_dict(
    buy, orient='index', columns=['名稱', '張數', '收盤價'])
sale_df = pd.DataFrame.from_dict(sale, orient='index', columns=[
                                 '名稱', '張數', '收盤價'])

if(category == "0"):
    print(date+"上市外資買賣超排行"+day+"日排行")
    buy_df.to_csv(date+"上市外資買超排行"+day+"日排行.csv", encoding='big5')
    sale_df.to_csv(date+"上市外資賣超排行"+day+"日排行.csv", encoding='big5')

else:
    print(date+"上櫃外資買賣超排行"+day+"日排行")
    buy_df.to_csv(date+"上櫃外資買超排行"+day+"日排行.csv", encoding='big5')
    sale_df.to_csv(date+"上櫃外資賣超排行"+day+"日排行.csv", encoding='big5')

print("買超排行")
print(tabulate(buy_df,headers='keys',tablefmt='psql'))
print("賣超排行")
print(tabulate(sale_df,headers='keys',tablefmt='psql'))