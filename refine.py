import sqlite3

conn = sqlite3.connect('refine.sqlite')
cur = conn.cursor()

cur.execute('DROP TABLE IF EXISTS Currency')
cur.execute('''CREATE TABLE IF NOT EXISTS Currency
    (id INTEGER PRIMARY KEY, 幣別_currency TEXT UNIQUE, 現金買入_cashbr REAL , 現金賣出_cashsr  REAL,
     即期買入_spotbr  REAL, 即期賣出_spotsr  REAL)''')

conn_1=sqlite3.connect('file:exchangert.sqlite?mode=ro', uri=True)
cur_1 = conn_1.cursor()
cur_1.execute('''SELECT 幣別_currency,現金買入_cashbr, 現金賣出_cashsr,即期買入_spotbr,即期賣出_spotsr,遠期10日買進_far10dbuy ,遠期10日賣出_10daysell,
遠期30日買進_far30dbuy ,遠期30日賣出_30daysell,遠期60日買進_far60dbuy ,遠期60日賣出_60daysell FROM Currency''')
print('=============================================')
#clean data:
#(1) remove the currency data which 現金買入_cashbr < input number
#(2) only keep the column about today's information
#(3) remove the data which contain None in it
text=list()
cashbr_criteria=input('Enter the minimum cashbr value:')
try:
  for content in cur_1:
     info=list()
     for i in content:
         info.append(i)
         if str(i)=='None' :
           info=list()
           break
     if len(info)==0:
       continue
     if info[1]<float(cashbr_criteria):
       continue
     cur.execute('INSERT OR IGNORE INTO Currency (幣別_currency,現金買入_cashbr,現金賣出_cashsr,即期買入_spotbr,即期賣出_spotsr) VALUES ( ?,?,?,?,? )', (info[0],info[1],info[2],info[3],info[4]))
  conn.commit()
except:
   print('Please insert a number')

   

