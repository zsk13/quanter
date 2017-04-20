# coding:utf-8

from sqlalchemy import create_engine
from sqlalchemy import VARCHAR
from sqlalchemy import Date
import tushare as ts
import sys
from quanter.models import *

engine = create_engine('mysql://root:123456@127.0.0.1/quanter?charset=utf8')

def get_stock():
    datas = stock_basic.objects.all()
    for data in datas:
        s = Stock()
        s.code = data.code
        s.name = data.name
        s.save()

def get_DayData():
    datas = stock_basic.objects.all().order_by('code')
    i = 0
    for data in datas:
        i += 1
        if i<=2863:
            continue
        code = data.code
        get_dailydata_by_code(code)

def get_dailydata_by_code(code):
    df = ts.get_h_data(code, start = "2014-01-01", end = "2017-05-01")
    try:
        df = df.rename(columns={"amount": "amt"})
    except:
        print code+"      error "
        return
    df['stock_id'] = code
    df.to_sql('quanter_daydata', engine, if_exists='append',dtype={'code':VARCHAR(50)})



def get_stock_basics():
    df = ts.get_stock_basics()
    df.to_sql('stock_basic',engine,if_exists='append',dtype={'code':VARCHAR(50)})


def get_hist_data():
    datas = stock_basic.objects.all()
    for data in datas:
        code = data.code
        get_hist_data_by_code(code)

def get_hist_data_by_code(code):
    df = ts.get_hist_data(code)
    df['code'] = code
    df.reset_index(drop = True)
    df.to_sql('quanter_dailydata',engine,if_exists='append',dtype={'date':Date,'code':VARCHAR(50)})

def get_hs300_data():
    #code=399300
    code = '399300'
    for i in range(13):
        start = str(2005+i)+"-01-01"
        if i==12:
            end = str(2005+i)+"-04-01"
        else:
            end = str(2006+i)+"-01-01"
        data = ts.get_h_data(code=code, index = True, start = start, end = end)
        dates = data.index
        querysetlist=[]
        for j in range(len(dates)):
            daily = dailydata()
            daily.code = code
            daily.date = dates[j]
            daily.open = data.loc[dates[j],'open']
            daily.close = data.loc[dates[j],'close']
            daily.high = data.loc[dates[j],'high']
            daily.low = data.loc[dates[j],'low']
            daily.volume = data.loc[dates[j],'volume']
            querysetlist.append(daily)
        dailydata.objects.bulk_create(querysetlist)
        

if __name__ == '__main__':
    # get_stock_basics()
    get_hist_data()