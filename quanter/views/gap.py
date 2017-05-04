from django.http import HttpResponse, Http404
from django import template
from django.shortcuts import render_to_response
from quanter.models import *
from quanter.forms import *
import json
from quanter.gapStrategy import GapStrategy,GapHelper

import datetime

def show_gap(request,code='SH603999'):
    stock = Stock.objects.get(code=code)
    stockData = []

    dayDatas = stock.daydata_set.order_by('date')
    recommendData = getRecommendStocks()
    paraList = getParaList()

    rawData = []
    for dayData in dayDatas:
        rawData.append([str(dayData.date),0])

    return render_to_response("gap.html",{
            'list': json.dumps(rawData),
            'stocks': json.dumps(stockData),
            'recommendData': json.dumps(recommendData),
            'paraList':json.dumps(paraList)
    })

def backTest_gap(request):
    start = request.GET.get('start')
    end = request.GET.get('end')
    breach = request.GET.get('breach')
    paraList = {'long':breach}
    idList_str = request.GET.get('idList')

    idList = idList_str.split(',')

    gap = GapStrategy('gap')
    gh = GapHelper(paraList)
    gap.setPara("2016-01-01","2016-03-05")
    gap.setHelper(gh)
    profitRate_day = gap.autobuy(idList)

    return HttpResponse(json.dumps({'profitRate_day':profitRate_day}),content_type="application/json")

    #return HttpResponse(json.dumps({'idList':idList}),content_type="application/json")

def getParaList():
    gap = GapStrategy('gap')
    paraList = gap.getRecommendPara()
    return paraList

def storeRecommendStocks_gap(request):
    start = request.GET.get('start')
    end = request.GET.get('end')
    breach = request.GET.get('breach')
    paraList = {'breach':breach}
    gap = GapStrategy('gap')
    gh = GapHelper(paraList)
    gap.setHelper(gh)

    gap.storeRecommendStock(start,end)

    #return HttpResponse(threek.storeRecommendStock(paraList,start,end))

def getRecommendStocks():
    gap = GapStrategy('gap')
    profitRateData = gap.getRecommendStock()
    recommendData = []
    for prd in profitRateData:
        st = prd.stock
        recommendData.append({'id':st.code,'name':st.name,'profit':prd.profitRate})

    return recommendData

def getRecord_gap(request):
    start = request.GET.get('start')
    end = request.GET.get('end')
    breach = request.GET.get('breach')
    paraList = {'breach':breach}
    gap = GapStrategy('gap')
    gh = GapHelper(paraList)
    gap.setHelper(gh)

    return HttpResponse(gap.storeRecommendStock(start,end))


