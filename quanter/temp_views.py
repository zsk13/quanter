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
    path = "/home/zsk/django/data/"
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
                dayData = DayData()
                print(row)
                if(row[1]=='NA'):
                    continue
                dayData.date = row[0]
                dayData.open_price = row[1]
                dayData.high = row[2]
                dayData.low = row[3]
                dayData.close = row[4]
                dayData.trade_status = ""
                dayData.volume = 1
                dayData.amt = 1
                dayData.stock = stock
                dayData.save()