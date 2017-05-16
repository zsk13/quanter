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

    user = request.user
    stockGroups = StockGroup.objects.filter(userId = user.id)
    stockGroups_info = []
    for sg in stockGroups:
        stockGroups_info.append({'id':sg.id,'name':sg.groupName})

    return render_to_response("gap.html",{
            'list': json.dumps(rawData),
            'stocks': json.dumps(stockData),
            'recommendData': json.dumps(recommendData),
            'paraList':json.dumps(paraList),
            'stockGroups':json.dumps(stockGroups_info),
    })

def findStock_gap(request):
    st_code = request.GET.get('st_code')
    st = Stock.objects.get(code = st_code)
    st_info = {'code':st.code,'name':st.name}
    return HttpResponse(json.dumps({'st_info':st_info}),content_type="application/json")

def filterStocks_gap(request):
    start = request.GET.get('start')
    end = request.GET.get('end')
    breach = request.GET.get('breach')
    groupId = request.GET.get('groupId')
    paraList = {'breach':breach}

    stocks = GroupContent.objects.filter(groupId_id = groupId)

    gap = GapStrategy('gap')
    gh = GapHelper(paraList)
    #gap.setPara("2016-01-01","2016-03-05",1000000)
    gap.setPara(start,end,1000000)
    gap.setHelper(gh)

    recommendData = []

    for st in stocks:
        idList = [st.stockCode]
        profitRate = gap.autobuy(idList)['profitRate']
        stock = Stock.objects.get(code = st.stockCode)
        recommendData.append({'id':stock.code,'name':stock.name,'profit':profitRate})


    return HttpResponse(json.dumps({'recommendData':recommendData}),content_type="application/json")

def backTest_gap(request):
    start = request.GET.get('start')
    end = request.GET.get('end')
    iniMoney = float(request.GET.get('iniMoney'))
    breach = request.GET.get('breach')
    paraList = {'breach':breach}
    idList_str = request.GET.get('idList')

    idList = idList_str.split(',')

    gap = GapStrategy('gap')
    gh = GapHelper(paraList)
    #gap.setPara("2016-01-19","2016-04-26",iniMoney)
    gap.setPara(start,end,iniMoney)
    gap.setHelper(gh)
    profitRate_day = gap.autobuy(idList)['profitRate_day']

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

    return HttpResponse(gap.getTradeRecord(start,end))


