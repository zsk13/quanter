from django.http import HttpResponse, Http404
from django import template
from django.shortcuts import render_to_response
from quanter.models import *
import json
from quanter.stockdata import *
from quanter.strategy import *
from quanter.backtest import *

def maSingleTest(request):
    return render_to_response("maStrategy_singleTest.html")

def maMultiTest(request):
    return render_to_response("maStrategy_multiTest.html")

def maAutoTest(request):
    return render_to_response("maStrategy_autoTest.html")

def maBackTest(request):
    code = request.GET.get('code')
    start = request.GET.get('start')
    end = request.GET.get('end')
    n = request.GET.get('n')
    m = request.GET.get('m')
    if n=='' or m=='':
        strategy = MAStrategy()
    else:
        strategy = MAStrategy(short_window=int(n),long_window=int(m))
    backTest = BackTest(code,start,end,strategy = strategy)

    jsonResult = backTest.getJsonResult()
    return HttpResponse(jsonResult,content_type="application/json")

def maMultiTestStockPool(request):
    groupId = request.GET.get('groupId')
    start = request.GET.get('start')
    end = request.GET.get('end')
    n = request.GET.get('n')
    m = request.GET.get('m')
    if n=='' or m=='':
        strategy = MAStrategy()
    else:
        strategy = MAStrategy(short_window=int(n),long_window=int(m))
    
    stockGroup = StockGroup.objects.get(id=groupId)
    groupContents = stockGroup.groupcontent_set.all()

    result = []
    for stock in groupContents:
        code = stock.stockCode
        backTest = BackTest(code,start,end,strategy = strategy)
        tempresult = backTest.getSimpleResult()
        result.append([code,tempresult])
    result = sorted(result,key = lambda x : x[1],reverse = True)
    jsonData = json.dumps(result)
    return HttpResponse(jsonData,content_type="application/json")

def maAutoFindParam(request):
    code = request.GET.get('code')
    start = request.GET.get('start')
    end = request.GET.get('end')
    n = request.GET.get('n')
    m = request.GET.get('m')
    print n
    ns = n.split(',')
    print ns
    ms = m.split(',')
    backTest = BackTest(code,start,end)
    result = []
    for ni in ns:
        for mi in ms:
            strategy = MAStrategy(int(ni),int(mi))
            backTest.setStrategy(strategy)
            tempresult = backTest.getSimpleResult()
            result.append([int(ni),int(mi),tempresult])
    result = sorted(result,key = lambda x : x[2], reverse=True)
    jsonData = json.dumps(result)
    return HttpResponse(jsonData,content_type="application/json")