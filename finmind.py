import requests
import csv
import json
import pandas as pd

#-----下載資料-----#
url = "https://api.finmindtrade.com/api/v4/data"
parameter = {
    "dataset": "TaiwanStockPrice",
    "data_id": "2317",
    "start_date": "2023-01-01"
}
r = requests.get(url, params=parameter)
data = r.json()
stock_deal_info = data["data"]

#-----把下載的json資料寫入csv檔案內-----#
with open('stock.csv','w+',encoding='utf-8') as file:
    writer = csv.DictWriter(
        file, fieldnames=["date", "stock_id", "Trading_Volume", "Trading_money", "open", "max", "min", "close", "spread", "Trading_turnover"])
    writer.writeheader()
    for row in stock_deal_info:
        writer.writerow(row)
        
#-----移除資料空白行-----#
with open("stock.csv","r",encoding="utf-8") as file2:
    reader=csv.reader(file2)
    data = list(reader)
    for i in range(len(data) - 1, -1, -1):
        if not data[i]:
            del data[i]
    with open('stock.csv', 'w', newline='') as fp:
        writer = csv.writer(fp)
        writer.writerows(data)

#-----從最後一筆開始讀取資料-----#
with open("stock.csv", "r") as f:
    reader = csv.reader(f)
    data=list(reader)
    for row in reversed(data):
        print(row)

#抓取最後180筆資料的date及close
data = pd.read_csv('stock.csv') #讀取row data檔案
tail_180=data.tail(180)
date=tail_180[["date"]]
close=tail_180[['close']]
volume=tail_180[['Trading_Volume']]

#-----計算5日均價值-----#
mov5=round(tail_180['close'].rolling(window=5).mean(),ndigits=2) 
mov5=list(mov5)
#-----計算20日均價值-----#
mov20=round(tail_180['close'].rolling(window=20).mean(),ndigits=2)
mov20=list(mov20)
#-----計算60日均價值-----#
mov60=round(tail_180['close'].rolling(window=60).mean(),ndigits=2)
mov60=list(mov60)

#-----計算5日平均成交量-----#
avg_volume_5=round(tail_180['Trading_Volume'].rolling(window=5).mean())
avg_volume_5=list(avg_volume_5)
#-----計算20日平均成交量-----#
avg_volume_20=round(tail_180['Trading_Volume'].rolling(window=20).mean())
avg_volume_20=list(avg_volume_20)
#-----計算60日平均成交量-----#
avg_volume_60=round(tail_180['Trading_Volume'].rolling(window=60).mean())
avg_volume_60=list(avg_volume_60)



#-----將計算出的均值寫入csv檔
mov=pd.DataFrame()
mov['日期']=date
mov['收盤價']=close
mov['5日移動均價']=mov5
mov['20日移動均價']=mov20
mov['60日移動均價']=mov60
mov['當日成交量']=volume
mov['5日平均成交量']=avg_volume_5
mov['20日平均成交量']=avg_volume_20
mov['60日平均成交量']=avg_volume_60
mov.to_csv('mov.csv')

#-----插入5/20/60日移動均價的前值-----#
data1 = pd.read_csv('mov.csv')
tail_180=data1.tail(180)
#-----原本欄位-----#
date=tail_180[["日期"]]
close=tail_180[['收盤價']]
mov5=tail_180[['5日移動均價']]
mov20=tail_180[['20日移動均價']]
mov60=tail_180[['60日移動均價']]
volume=tail_180[['當日成交量']]
avg_volume_5=tail_180[['5日平均成交量']]
avg_volume_20=tail_180[['20日平均成交量']]
avg_volume_60=tail_180[["60日平均成交量"]]

#-----新增加的欄位-----#
prev_mov_5=data1[['5日移動均價']]
prev_mov_5=prev_mov_5.shift(periods=1) #取得前一日的5日移動均價
prev_mov_20=data1[['20日移動均價']]
prev_mov_20=prev_mov_20.shift(periods=1) #取得前一日的20日移動均價
prev_mov_60=data1[['60日移動均價']]
prev_mov_60=prev_mov_60.shift(periods=1) #取得前一日的60日移動均價

mov=pd.DataFrame()
mov['日期']=date
mov['收盤價']=close
mov['5日移動均價']=mov5
mov['5日移動均價'].fillna(0,inplace=True) #將欄位數值出現Nan補為0.00
mov['prev_5日移動均價']=prev_mov_5
mov['prev_5日移動均價'].fillna(0,inplace=True) #將欄位數值出現Nan補為0.00
mov['20日移動均價']=mov20
mov['20日移動均價'].fillna(0,inplace=True) #將欄位數值出現Nan補為0.00
mov['prev_20日移動均價']=prev_mov_20
mov['prev_20日移動均價'].fillna(0,inplace=True) #將欄位數值出現Nan補為0.00
mov['60日移動均價']=mov60
mov['60日移動均價'].fillna(0,inplace=True) #將欄位數值出現Nan補為0.00
mov['prev_60日移動均價']=prev_mov_60
mov['prev_60日移動均價'].fillna(0,inplace=True) #將欄位數值出現Nan補為0.00
mov['當日成交量']=volume
mov['5日平均成交量']=avg_volume_5
mov['5日平均成交量'].fillna(0,inplace=True) #將欄位數值出現Nan補為0.00
mov['20日平均成交量']=avg_volume_20
mov['20日平均成交量'].fillna(0,inplace=True) #將欄位數值出現Nan補為0.00
mov['60日平均成交量']=avg_volume_60
mov['60日平均成交量'].fillna(0,inplace=True) #將欄位數值出現Nan補為0.00
mov.to_csv('mov.csv',index=False)


#-----繪製六十日K棒圖-----#
plt.rc("font", family="Microsoft JhengHei")  # 微軟正黑體
import csv
import pandas as pd
reader = pd.read_csv("stock.csv",encoding="utf-8")
reader_last_10dataframe = reader.tail(60)
info = reader_last_10dataframe.values
fig = plt.figure(figsize=(16, 9))
for row in info:
    # print(row)
    date=row[0]
    open_price=float(row[4])
    close_price=float(row[7])
    hightest=float(row[5])
    lowest=float(row[6])
    # 決定 陰線(下跌)  或 陽線(上漲)
    color="green"
    if close_price > open_price:
        color="red"
    # 畫陰陽線
    plt.bar(
        date,
        abs(open_price - close_price),
        bottom=min(open_price, close_price),
        color=color, width=0.5
    )
    # 畫影線 
    plt.bar(date, hightest - lowest, bottom=lowest,color=color, width=0.1)
fig.autofmt_xdate(rotation=45)
#plt.show()
plt.savefig('K-stock.jpeg')
