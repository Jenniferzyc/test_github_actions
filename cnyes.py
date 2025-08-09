# coding: utf-8
import requests
import pandas as pd
import datetime as dt
import json
data = []
url = "https://api.cnyes.com/media/api/v1/newslist/category/headline" # 新聞連結 # 連結問號前面是url，後面是參數
payload = {"page":1, 
           "limit":30, 
           "isCategoryHeadline":1, 
           "startAt":int((dt.datetime.today() - dt.timedelta(days = 10)).timestamp()), 
           "endAt":int(dt.datetime.today().timestamp())} # 參數
res = requests.get(url, params = payload) # 連線鉅亨網
jd = json.loads(res.text) # 解析json轉成dict
data.append(pd.DataFrame(jd['items']['data']))

for i in range(2, jd['items']['last_page'] + 1):
    print(i)
    payload["page"] = i
    res = requests.get(url, params = payload) # 連線鉅亨網
    jd = json.loads(res.text) # 解析json轉成dict
    data.append(pd.DataFrame(jd['items']['data']))
    
df = pd.concat(data, ignore_index = True) # 取出新聞資料
df = df[['newsId', 'title', 'summary']] # 取出特定欄位
df['link'] = df['newsId'].apply(lambda x: 'https://m.cnyes.com/news/id/' + str(x)) # 建立連結
df.to_csv('news.csv', encoding='utf-8-sig', index = False) # 調參index是指將第一行index不要顯示出來，要不然預設會顯示
# df.to_excel('news.xlsx', index = False)                    # 調參index是指將第一行index不要顯示出來，要不然預設會顯示
print(df)

