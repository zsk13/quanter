from django.http import HttpResponse, Http404
from django import template
from django.shortcuts import render_to_response
from quanter.models import *
import json
from quanter.stockdata import *
from quanter.strategy import *
from quanter.backtest import *

def biasSingleTest(request):
    return render_to_response("biasStrategy_singleTest.html")

def biasMultiTest(request):
    return render_to_response("biasStrategy_multiTest.html")


def biasBackTest(request):
    code = request.GET.get('code')
    start = request.GET.get('start')
    end = request.GET.get('end')
    strategy = BIASStrategy()
    backTest = BackTest(code,start,end,strategy = strategy)

    jsonResult = backTest.getJsonResult()
    return HttpResponse(jsonResult,content_type="application/json")

def biasMultiTestStockPool(request):
    start = request.GET.get('start')
    end = request.GET.get('end')

    strategy = BIASStrategy()
    email = request.user.email
    user = User.objects.get(email=email)
    stockpool =user.stockpool_set.all()

    result = []
    for stock in stockpool:
        code = stock.stockCode
        backTest = BackTest(code,start,end,strategy = strategy)
        tempresult = backTest.getSimpleResult()
        result.append([code,tempresult])
    result = sorted(result,key = lambda x : x[1],reverse = True)
    jsonData = json.dumps(result)
    return HttpResponse(jsonData,content_type="application/json")

