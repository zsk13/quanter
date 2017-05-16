import datetime
from django.http import HttpResponse, Http404
from quanter.stockdata import *
import json
from django.shortcuts import render_to_response
from quanter.models import *
from users.models import *


def showStock(request, code = "SH603999"):
    # start = (datetime.datetime.now() - datetime.timedelta(days = 100)).strftime("%Y-%m-%d")
    # end = datetime.datetime.now().strftime("%Y-%m-%d")
    dataService = StockDataFactory.getStockDataService()
    dayDatas = dataService.getStockDataAsObject(code)
    
    rawData = []
    for dayData in dayDatas:
        rawData.append([str(dayData.date),dayData.open,dayData.close,dayData.high,dayData.low])
    
    return render_to_response("stockgroup_showStock.html",{
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
    groupId = request.GET.get('groupId')
    code = request.GET.get('code')
    user = request.user
    stockgroup =user.stockgroup_set.get(id=groupId)
    content = stockgroup.groupcontent_set.filter(stockCode = code)
    if len(content)==0:
        s = GroupContent()
        s.groupId = stockgroup
        s.stockCode = code
        s.save()
        rawData = "success"
    else:
        rawData = "exist"
    return HttpResponse(json.dumps(rawData),content_type="application/json")

def addStockGroup(request):
    groupName = request.GET.get('groupName')
    user = request.user
    group = StockGroup()
    group.groupName = groupName
    group.userId = user
    group.save()
    return HttpResponse(json.dumps({'id':group.id,'groupName':group.groupName}),content_type="application/json")

def manageStockGroups(request):
    return render_to_response("stockgroup_manageStockGroups.html")

def getStockGroups(request):
    user = request.user
    stockgroup =user.stockgroup_set.all()
    rawData = []
    for s in stockgroup:
        group = {}
        group['id'] = s.id
        group['groupName'] = s.groupName
        rawData.append(group)
    return HttpResponse(json.dumps(rawData),content_type="application/json")

def showStockGroup(request):
    groupId = request.GET.get('groupId')
    stockGroup = StockGroup.objects.get(id = groupId)
    groupContents = stockGroup.groupcontent_set.all()
    result = []
    for stock in groupContents:
        result.append(stock.stockCode)
    return render_to_response("stockgroup_showStockGroup.html",{
        'list': json.dumps(result),
    })

def deleteStockGroup(request):
    groupId = request.GET.get('groupId')
    stockGroup = StockGroup.objects.get(id=groupId)
    groupContents = stockGroup.groupcontent_set.all()
    groupContents.delete();
    stockGroup.delete();

    return HttpResponse(json.dumps("success"),content_type="application/json")

def deleteStock(request):
    groupId = request.GET.get('groupId')
    code = request.GET.get('code')
    stockGroup = StockGroup.objects.get(id=groupId)
    groupContents = stockGroup.groupcontent_set.filter(stockCode=code)
    if len(groupContents)==0:
        rawData = "not exist"
    else:
        groupContents.delete()
        rawData = "success"
    return HttpResponse(json.dumps(rawData),content_type="application/json")