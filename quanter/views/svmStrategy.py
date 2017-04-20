from django.http import HttpResponse, Http404
from django import template
from django.shortcuts import render_to_response
from quanter.models import *
from quanter.forms import *
#from sklearn import svm
import json
import numpy as np
from quanter.backTesting import *
from quanter.svm import *
def svmStrategy(request,code='000001', start='2014-01-01', end='2016-01-01'):

    return render_to_response("svmStrategy.html")

def svm_training(request, year=2014,quarter=1):
    resultCode = []
    resultName = []
    # year = request.GET.get('year')
    # quarter = request.GET.get('quarter')
    data = Data(year, quarter)
    trainingData = data.get_report_data_from_db()
    svm1 = SVMStrategy()
    svm1.svmTraining(trainingData[1],trainingData[2])
    data = Data(int(year)+1,quarter)
    predict_data = data.get_report_data_from_db()
    result = svm1.svmPredict(predict_data[1])
    sorted_result = np.argsort(result)

    for i in range(10):
        resultCode.append(predict_data[0][sorted_result[-i]])
        resultName.append(predict_data[3][sorted_result[-i]])
    
    return HttpResponse(json.dumps({'resultCode':resultCode,'resultName':resultName}),content_type="application/json") 
