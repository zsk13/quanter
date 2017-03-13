from django.http import HttpResponse, Http404
from django import template
from django.shortcuts import render_to_response
from quanter.models import *
from quanter.forms import *
import json

def show(request,code='SH603901'):
    stock = Stock.objects.get(code=code)
    stocks = Stock.objects.all()
    stockData = []
    recommendData = []
    for st in stocks:
        stockData.append({'id':st.code,'name':st.name})
        recommendData.append({'id':st.code,'name':st.name,'recommend':5})

    dayDatas = stock.daydata_set.order_by('date')

    rawData = []
    for dayData in dayDatas:
        rawData.append([str(dayData.date),dayData.open_price,dayData.close,dayData.high,dayData.low])
    
    return render_to_response("3k5k.html",{
            'list': json.dumps(rawData),
            'stocks': json.dumps(stockData),
            'recommendData': json.dumps(recommendData)
    })