from django.http import HttpResponse, Http404
from django import template
from django.shortcuts import render_to_response
from quanter.models import *
from quanter.forms import *
import json
import numpy as np
from quanter.stockdata import *
from quanter.strategy import *
from quanter.backtest import *
def svmStrategy(request,code='000001', start='2014-01-01', end='2016-01-01'):
    print request.user
    return render_to_response("svmStrategy.html")

def svm_training(request):
    code = request.GET.get('code')
    start = request.GET.get('start')
    end = request.GET.get('end')

    strategy = SVMStrategy(ratio)
    backTest = BackTest(code,start,end,strategy = strategy)

    jsonResult = backTest.getJsonResult()
    return HttpResponse(jsonResult,content_type="application/json")

    # resultCode = []
    # resultName = []
    # # year = request.GET.get('year')
    # # quarter = request.GET.get('quarter')
    # data = Data(year, quarter)
    # trainingData = data.get_report_data_from_db()
    # svm1 = SVMStrategy()
    # svm1.svmTraining(trainingData[1],trainingData[2])
    # data = Data(int(year)+1,quarter)
    # predict_data = data.get_report_data_from_db()
    # result = svm1.svmPredict(predict_data[1])
    # sorted_result = np.argsort(result)

    # for i in range(10):
    #     resultCode.append(predict_data[0][sorted_result[-i]])
    #     resultName.append(predict_data[3][sorted_result[-i]])
    
    # return HttpResponse(json.dumps({'resultCode':resultCode,'resultName':resultName}),content_type="application/json") 

def svm_result(request):
    code = request.GET.get('code')
    start = request.GET.get('start')
    end = request.GET.get('end')
    verifystart = request.GET.get('verifystart')
    verifyend = request.GET.get('verifyend')
    strategy = SVMStrategy(code+"_"+start+"_"+end,code,start,end)

    email = request.user.email
    user = User.objects.get(email=email)
    stockpool =user.stockpool_set.all()

    result = []
    for stock in stockpool:
        code = stock.stockCode
        backTest = BackTest(code,verifystart,verifyend,strategy = strategy)
        tempresult = backTest.getSimpleResult()
        result.append([code,tempresult])
    result = sorted(result,key = lambda x : x[1],reverse = True)
    jsonData = json.dumps(result)
    return HttpResponse(jsonData,content_type="application/json")

def svm_test(request):
    code = request.GET.get('code')
    start = request.GET.get('start')
    end = request.GET.get('end')
    testcode = request.GET.get('testcode')
    teststart = request.GET.get('teststart')
    testend = request.GET.get('testend')

    strategy = SVMStrategy(code+"_"+start+"_"+end)
    backTest = BackTest(testcode,teststart,testend,strategy = strategy)
    
    jsonResult = backTest.getJsonResult()
    return HttpResponse(jsonResult,content_type="application/json")