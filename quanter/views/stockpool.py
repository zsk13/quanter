import datetime
from django.http import HttpResponse, Http404
from quanter.stockdata import *
import json
from django.shortcuts import render_to_response
from quanter.models import *
from users.models import *


def showStock(request, code = "300002"):
    # start = (datetime.datetime.now() - datetime.timedelta(days = 100)).strftime("%Y-%m-%d")
    # end = datetime.datetime.now().strftime("%Y-%m-%d")
    dataService = StockDataFactory.getStockDataService()
    dayDatas = dataService.getStockDataAsObject(code)
    
    rawData = []
    for dayData in dayDatas:
        rawData.append([str(dayData.date),dayData.open,dayData.close,dayData.high,dayData.low])
    
    return render_to_response("stockpool_showStock.html",{
            'list': json.dumps(rawData),
    })

def searchStock(request):
    code = request.GET.get('code')
    dataService = StockDataFactory.getStockDataService()
    dayDatas = dataService.getStockDataAsObject(code)
    
    rawData = []
    for dayData in dayDatas:
        rawData.append([str(dayData.date),dayData.open,dayData.close,dayData.high,dayData.low])
    
    return HttpResponse(json.dumps(rawData),content_type="application/json")
    
def addStock(request):
    code = request.GET.get('code')
    email = request.user.email
    user = User.objects.get(email=email)
    stockpool =user.stockpool_set.filter(stockCode=code)
    if len(stockpool)==0:
        s = StockPool()
        s.userId = user
        s.stockCode = code
        s.save()
        rawData = "success"
    else:
        rawData = "exist"
    return HttpResponse(json.dumps(rawData),content_type="application/json")

def showStockPool(request):
    email = request.user.email
    user = User.objects.get(email=email)
    stockpool =user.stockpool_set.all()
    result = []
    for stock in stockpool:
        result.append(stock.stockCode)
    return render_to_response("stockpool_showStockPool.html",{
        'list': json.dumps(result),
    })

def deleteStock(request):
    code = request.GET.get('code')
    email = request.user.email
    user = User.objects.get(email=email)
    stockpool =user.stockpool_set.filter(stockCode=code)
    if len(stockpool)==0:
        rawData = "not exist"
    else:
        stockpool.delete()
        rawData = "success"
    return HttpResponse(json.dumps(rawData),content_type="application/json")