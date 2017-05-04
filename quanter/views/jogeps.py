from django.http import HttpResponse, Http404
from django import template
from django.shortcuts import render_to_response
from quanter.models import *
from quanter.forms import *
import json
from quanter.jogepsStrategy import JogepsStrategy,JogepsHelper

import datetime

def show_jogeps(request,code='SH603999'):
    stock = Stock.objects.get(code=code)
    stockData = []

    dayDatas = stock.daydata_set.order_by('date')
    recommendData = getRecommendStocks()
    paraList = getParaList()

    rawData = []
    for dayData in dayDatas:
        rawData.append([str(dayData.date),0])

    return render_to_response("jogeps.html",{
            'list': json.dumps(rawData),
            'stocks': json.dumps(stockData),
            'recommendData': json.dumps(recommendData),
            'paraList':json.dumps(paraList)
    })

def backTest_jogeps(request):
    start = request.GET.get('start')
    end = request.GET.get('end')
    long = request.GET.get('long')
    short = request.GET.get('short')
    paraList = {'long':long,'short':short}
    idList_str = request.GET.get('idList')

    idList = idList_str.split(',')

    jogeps = JogepsStrategy('jogeps')
    jgh = JogepsHelper(paraList)
    jogeps.setPara("2016-01-01","2016-03-05")
    jogeps.setHelper(jgh)
    profitRate_day = jogeps.autobuy(idList)

    return HttpResponse(json.dumps({'profitRate_day':profitRate_day}),content_type="application/json")

    #return HttpResponse(json.dumps({'idList':idList}),content_type="application/json")

def getParaList():
    jogeps = JogepsStrategy('jogeps')
    paraList = jogeps.getRecommendPara()
    return paraList

def storeRecommendStocks_jogeps(request):
    start = request.GET.get('start')
    end = request.GET.get('end')
    long = request.GET.get('long')
    short = request.GET.get('short')
    paraList = {'long':long,'short':short}
    jogeps = JogepsStrategy('jogeps')
    jgh = JogepsHelper(paraList)
    jogeps.setHelper(jgh)

    jogeps.storeRecommendStock(start,end)

    #return HttpResponse(threek.storeRecommendStock(paraList,start,end))

def getRecommendStocks():
    jogeps = JogepsStrategy('jogeps')
    profitRateData = jogeps.getRecommendStock()
    recommendData = []
    for prd in profitRateData:
        st = prd.stock
        recommendData.append({'id':st.code,'name':st.name,'profit':prd.profitRate})

    return recommendData

def getRecord_jogeps(request):
    start = request.GET.get('start')
    end = request.GET.get('end')
    long = request.GET.get('long')
    short = request.GET.get('short')
    paraList = {'long':long,'short':short}
    jogeps = JogepsStrategy('jogeps')
    jgh = JogepsHelper(paraList)
    jogeps.setHelper(jgh)

    return HttpResponse(jogeps.storeRecommendStock(start,end))

