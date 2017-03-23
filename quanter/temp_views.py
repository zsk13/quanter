# encoding: UTF-8
# Create your views here.
from django.http import HttpResponse, Http404
from django import template
from django.shortcuts import render_to_response
from quanter.models import *
from quanter.forms import *
import csv
import os

def hello(request):
    return HttpResponse("hello world")

def hello1(request, num):
    try:
        num = int(num)
        return HttpResponse(num)
    except ValueError:
        return Http404()

def form(request):
    if request.method == 'POST':
        form =  Mybook(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            title = data['name']
        return HttpResponse(title)

    form = Mybook()
    return render_to_response('1.html',{'form':form})

def views(request, template_name):
    return render_to_response(template_name)

def jsonData(request, id):
    
    return JsonResponse()

def initData(request):
    path = "E:/FinalDesign/daydata/"
    for parent,dirnames,filenames in os.walk(path): 
        for name in filenames:
            csv_reader = csv.reader(open(path+name))
            strs = name.split('.')
            code = strs[1]+strs[0]
            stock = Stock()
            stock.code = code
            stock.name = code
            stock.save()
            for row in csv_reader:
                if row[0] == "date":
                    continue
                if row[0] < "2016-01-01":
                    continue
                dayData = DayData()
                if(row[6]=='NA'):
                    continue
                dayData.date = row[0]
                dayData.open = row[1]
                dayData.high = row[2]
                dayData.low = row[3]
                dayData.close = row[4]
                dayData.status = row[5].decode('gb2312').encode('utf8')
                dayData.volume = row[6]
                dayData.amt = row[7]
                dayData.stock = stock
                dayData.save()

