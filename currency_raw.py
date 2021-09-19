from bs4 import BeautifulSoup
import urllib.request
import sqlite3
import ssl

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

conn = sqlite3.connect('exchangert.sqlite')
cur = conn.cursor()
cur.executescript('''DROP TABLE IF EXISTS Currency;''')

cur.execute('''CREATE TABLE IF NOT EXISTS Currency
    (id INTEGER PRIMARY KEY, 幣別_currency TEXT UNIQUE, 現金買入_cashbr REAL , 現金賣出_cashsr  REAL,
     即期買入_spotbr  REAL, 即期賣出_spotsr  REAL, 遠期10日買進_far10dbuy  REAL,遠期10日賣出_10daysell  REAL)''')


url=input("enter the url:")
request=urllib.request.Request(url, headers = {
  "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:92.0) Gecko/20100101 Firefox/92.0"})
document=urllib.request.urlopen(request,context=ctx)
pos=url.rfind('/')
web = url[:pos]

data=document.read().decode()
root=BeautifulSoup(data,"html.parser") 
content=root('tbody')


for i in content:
   con1=i('tr')
   
print("=================================================")
webs=list()
for i in con1:
  currency_tit=i.find_all('div',class_='hidden-phone print_show')
  cashchangert=i.find_all('td',class_='rate-content-cash text-right print_hide')
  spotchangert=i.find_all('td',class_='rate-content-sight text-right print_hide')
  newur=i.find_all('a')

  newurl=(web+newur[0].get('href')) #記錄遠期匯率網址相對位置
  webs.append(newurl) #絕對網址
  currency=currency_tit[0].text.strip()
  cashbr=cashchangert[0].text.strip()
  try:
    a=float(cashbr)
  except:
    cashbr=None
  cashsr=cashchangert[1].text.strip()
  try:
    a=float(cashsr)
  except:
    cashsr=None
  spotbr=spotchangert[0].text.strip()
  try:
    a=float(spotbr)
  except:
    spotbr=None
  spotsr=spotchangert[1].text.strip()
  try:
    a=float(spotsr)
  except:
    spotsr=None
  
  cur.execute('INSERT OR IGNORE INTO Currency (幣別_currency,現金買入_cashbr,現金賣出_cashsr,即期買入_spotbr,即期賣出_spotsr) VALUES ( ?,?,?,?,? )', (currency,cashbr,cashsr,spotbr,spotsr))
conn.commit()
#open other web\ from current website to catch past 10days average data of each currency
count=1
for web in webs: 
  request=urllib.request.Request(web, headers = {
  "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:92.0) Gecko/20100101 Firefox/92.0"})
  document=urllib.request.urlopen(request,context=ctx)
  data=document.read().decode()
  root=BeautifulSoup(data,"html.parser") 
  content=root('tbody')
  for i in content:
   con1=i('tr')
  for i in con1:
   far=i.find_all('td',class_='text-right')

   far10b=far[0].text.strip()
   try:
    a=float(far10b)
   except:
    far10b=None
   far10s=far[1].text.strip()
   try:
    a=float(far10s)
   except:
    far10s=None
    
   if far10b !=None or far10b !=None:
     break
  cur.execute('UPDATE Currency SET (遠期10日買進_far10dbuy,遠期10日賣出_10daysell )=(?,?) WHERE id=?', (far10b,far10s,count) )
  #在現有database項目中更新資料
  count+=1
conn.commit()
  # print(far10b,far10s)