from django.http import HttpResponse, Http404
from django import template
from django.shortcuts import render_to_response
from quanter.models import *
import json
from quanter.stockdata import *
from quanter.strategy import *
from quanter.backtest import *

def customSingleTest(request):
    return render_to_response("customStrategy_singleTest.html")

def customMultiTest(request):
    return render_to_response("customStrategy_multiTest.html")

# def customAutoTest(request):
#     return render_to_response("customStrategy_autoTest.html")

def customBackTest(request):
    code = request.GET.get('code')
    start = request.GET.get('start')
    end = request.GET.get('end')
    buy = request.GET.get('buy')
    sell = request.GET.get('sell')

    strategy = CustomStrategy(buy,sell)
    backTest = BackTest(code,start,end,strategy = strategy)

    jsonResult = backTest.getJsonResult()
    return HttpResponse(jsonResult,content_type="application/json")

def customMultiTestStockPool(request):
    start = request.GET.get('start')
    end = request.GET.get('end')
    buy = request.GET.get('buy')
    sell = request.GET.get('sell')
    groupId = request.GET.get('groupId')
   
    strategy = CustomStrategy(buy,sell)

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

# def customAutoFindParam(request):
#     code = request.GET.get('code')
#     start = request.GET.get('start')
#     end = request.GET.get('end')
#     buy = request.GET.get('buy')
#     sell = request.GET.get('sell')
    
#     ns = n.split(',')
#     ms = m.split(',')
#     backTest = BackTest(code,start,end)
#     result = []
#     for ni in ns:
#         for mi in ms:
#             strategy = CustomStrategy(int(ni),int(mi))
#             backTest.setStrategy(strategy)
#             tempresult = backTest.getSimpleResult()
#             result.append([int(ni),int(mi),tempresult])
#     result = sorted(result,key = lambda x : x[2], reverse=True)
#     jsonData = json.dumps(result)
#     return HttpResponse(jsonData,content_type="application/json")