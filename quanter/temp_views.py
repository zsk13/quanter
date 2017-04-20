# encoding: UTF-8
# Create your views here.
from django.http import HttpResponse, Http404
from django import template
from django.shortcuts import render_to_response
from quanter.models import *
from quanter.forms import *
import MySQLdb
from sqlalchemy import create_engine
import pandas as pd
import numpy as np
import csv
import os
import datetime

def hello(request):
    return HttpResponse("hello world")

def hello1(request, num):
    try:
        num = int(num)
        return HttpResponse(num)
    except ValueError:
        return Http404()

def form(request):
    if request.method == 'POST':
        form =  Mybook(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            title = data['name']
        return HttpResponse(title)

    form = Mybook()
    return render_to_response('1.html',{'form':form})

def views(request, template_name):
    return render_to_response(template_name)

def jsonData(request, id):
    
    return JsonResponse()

def filterStockPool(request):
    stocksInpool = 0

    stocks = Stock.objects.all()
    for stock in stocks:
        code = stock.code
        alldayData = DayData.objects.filter(stock_id = code).order_by('date')
        if alldayData.count() == 0:
            stock.isInPool = False
            stock.save()
            continue
        min_date = alldayData[0].date

        if min_date <> datetime.date(2015,7,1) or alldayData.filter(status__contains = '停牌', date__gt = datetime.date(2015,12,9)).count() > 0:
            stock.isInPool = False
            stock.save()
        else:
            stock.isInPool = True
            stock.save()
            stocksInpool += 1
    return HttpResponse(stocksInpool)

def initdayData(request):
    path = "E:/FinalDesign/daydata/"
    for parent,dirnames,filenames in os.walk(path): 
        for name in filenames:
            csv_reader = csv.reader(open(path+name))
            strs = name.split('.')
            code = strs[1]+strs[0]
            stock = Stock()
            stock.code = code
            stock.name = code
            stock.save()
            for row in csv_reader:
                if row[0] == "date":
                    continue
                if row[0] < "2015-07-01" or row[0] > "2016-01-01":
                    continue
                dayData = DayData()
                if(row[6]=='NA'):
                    continue
                dayData.date = row[0]
                dayData.open = row[1]
                dayData.high = row[2]
                dayData.low = row[3]
                dayData.close = row[4]
                dayData.status = row[5].decode('gb2312').encode('utf8')
                dayData.volume = row[6]
                dayData.amt = row[7]
                dayData.stock = stock
                dayData.save()

def initmaData(request):
    conn = MySQLdb.connect(host="localhost",user="root",passwd="123456",db="quanter",charset="utf8")
    engine = create_engine('mysql://root:123456@localhost/quanter?charset=utf8')
    sql_getStocks = "select * from quanter_stock where isInPool = 1"
    df_stock = pd.read_sql(sql_getStocks,conn)
    codeList = df_stock['code']

    cur_id = 1
    df_result = pd.DataFrame(columns=['id','date','ma5','ma10','ma20','ma60','ma120','stock_id'])
    code_num = 0

    for code in codeList:
        code_num = code_num+1
        sql_getDaydata = "select id,date,close,stock_id from quanter_daydata where stock_id = '%s' order by date ASC" % (code)
        df_dayData = pd.read_sql(sql_getDaydata,conn)

        df_dayData['ma5'] = df_dayData['close'].rolling(5).mean()
        df_dayData['ma10'] = df_dayData['close'].rolling(10).mean()
        df_dayData['ma20'] = df_dayData['close'].rolling(20).mean()
        df_dayData['ma60'] = df_dayData['close'].rolling(60).mean()
        df_dayData['ma120'] = df_dayData['close'].rolling(120).mean()

        df_dayData = df_dayData[df_dayData.date >= datetime.date(2016,1,1) ]
        row_num = df_dayData.shape[0]
        df_dayData['id'] = pd.Series(np.arange(cur_id,cur_id+row_num,1),index=df_dayData.index)

        del df_dayData['close']

        df_result = df_result.append(df_dayData)

        cur_id = cur_id+row_num

    df_result.to_sql('quanter_madata',engine,index=False,if_exists='append',chunksize=1000)
    return HttpResponse(code_num)

def initKDJData(request):
    conn = MySQLdb.connect(host="localhost",user="root",passwd="123456",db="quanter",charset="utf8")
    engine = create_engine('mysql://root:123456@localhost/quanter?charset=utf8')
    sql_getStocks = "select * from quanter_stock where isInPool = 1"
    df_stock = pd.read_sql(sql_getStocks,conn)
    codeList = df_stock['code']

    cur_id = 1
    df_result = pd.DataFrame(columns=['id','date','RSV','K','D','J','stock_id'])
    code_num = 0

    for code in codeList:

        code_num = code_num+1
        sql_getDaydata = "select id,date,close,low,high,stock_id from quanter_daydata where stock_id = '%s' order by date ASC" % (code)
        df_dayData = pd.read_sql(sql_getDaydata,conn)

        df_dayData['RSV'] = (df_dayData['close'] - df_dayData['low'].rolling(9).min()) / (df_dayData['high'].rolling(9).max() - df_dayData['low'].rolling(9).min())*100
        df_dayData['K'] = df_dayData['RSV'].rolling(3).mean()
        df_dayData['D'] = df_dayData['K'].rolling(3).mean()
        df_dayData['J'] = 3*df_dayData['D'] - 2*df_dayData['K']

        df_dayData = df_dayData[df_dayData.date >= datetime.date(2016,1,1) ]
        row_num = df_dayData.shape[0]
        df_dayData['id'] = pd.Series(np.arange(cur_id,cur_id+row_num,1),index=df_dayData.index)

        del df_dayData['close']
        del df_dayData['low']
        del df_dayData['high']

        df_result = df_result.append(df_dayData)

        cur_id = cur_id+row_num

    df_result.to_sql('quanter_kdjdata',engine,index=False,if_exists='append',chunksize=1000)
    #df_result.to_sql('test',engine,index=False,if_exists='append',chunksize=1000)
    #return HttpResponse(df_dayData['D'])




