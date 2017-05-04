from django.http import HttpResponse, Http404
from django import template
from django.shortcuts import render_to_response
from quanter.models import *
from quanter.forms import *
import json
from quanter.threekStrategy import ThreekStrategy,KLineHelper

import datetime

def show_3k5k(request,code='SH603999'):
    stock = Stock.objects.get(code=code)
    stockData = []

    dayDatas = stock.daydata_set.order_by('date')
    recommendData = getRecommendStocks()
    paraList = getParaList()

    rawData = []
    for dayData in dayDatas:
        rawData.append([str(dayData.date),0])
    
    return render_to_response("3k5k.html",{
            'list': json.dumps(rawData),
            'stocks': json.dumps(stockData),
            'recommendData': json.dumps(recommendData),
            'paraList':json.dumps(paraList)
    })
def backTest_3k5k(request):
    start = request.GET.get('start')
    end = request.GET.get('end')
    long = request.GET.get('long')
    short = request.GET.get('short')
    mid = request.GET.get('mid')
    mini = request.GET.get('mini')
    paraList = {'long':long,'short':short,'mid':mid,'mini':mini}
    idList_str = request.GET.get('idList')

    idList = idList_str.split(',')

    threek = ThreekStrategy('3k5k')
    klh = KLineHelper(paraList)
    threek.setPara("2016-01-01","2016-03-05")
    threek.setHelper(klh)
    profitRate_day = threek.autobuy(idList)

    return HttpResponse(json.dumps({'profitRate_day':profitRate_day}),content_type="application/json")

    #return HttpResponse(json.dumps({'idList':idList}),content_type="application/json")

def getParaList():
    threek = ThreekStrategy('3k5k')
    paraList = threek.getRecommendPara()
    return paraList

def storeRecommendStocks_3k5k(request):
    start = request.GET.get('start')
    end = request.GET.get('end')
    long = request.GET.get('long')
    short = request.GET.get('short')
    mid = request.GET.get('mid')
    mini = request.GET.get('mini')
    paraList = {'long':long,'short':short,'mid':mid,'mini':mini}
    threek = ThreekStrategy('3k5k')
    klh = KLineHelper(paraList)
    threek.setHelper(klh)

    threek.storeRecommendStock(start,end)

    #return HttpResponse(threek.storeRecommendStock(paraList,start,end))

def getRecommendStocks():
    threek = ThreekStrategy('3k5k')
    profitRateData = threek.getRecommendStock()
    recommendData = []
    for prd in profitRateData:
        st = prd.stock
        recommendData.append({'id':st.code,'name':st.name,'profit':prd.profitRate})

    return recommendData

def getRecord_3k5k(request):
    start = request.GET.get('start')
    end = request.GET.get('end')
    long = request.GET.get('long')
    short = request.GET.get('short')
    mid = request.GET.get('mid')
    mini = request.GET.get('mini')
    paraList = {'long':long,'short':short,'mid':mid,'mini':mini}
    threek = ThreekStrategy('3k5k')
    klh = KLineHelper(paraList)
    threek.setHelper(klh)

    return HttpResponse(threek.storeRecommendStock(start,end))
