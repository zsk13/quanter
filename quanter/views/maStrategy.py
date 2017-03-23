from django.http import HttpResponse, Http404
from django import template
from django.shortcuts import render_to_response
from quanter.models import *
from quanter.forms import *
import json
from quanter.backTesting import *
def maStrategy(request,code='000001', start='2014-01-01', end='2015-01-01'):
    standard_bars = tushare.get_hist_data("hs300",start=start, end=end).sort_index()
    standard_bars['close'][:] = (standard_bars['close'][:] - standard_bars['open'][0])/standard_bars['open'][0]
    bars = tushare.get_hist_data(code,start=start, end=end).sort_index()
    

    test_strategy = MAStrategy(bars)
    signals = test_strategy.gen_signal()
    test_trade = MATrade(bars,signals)
    capital = test_trade.trade_tracing() 
    return render_to_response("strategy.html",{
            'dateData': capital['yieldRate'].to_json(orient='split'),
            'yieldRateData': capital['yieldRate'].to_json(orient='split'),
            'standardData': standard_bars['close'].to_json(orient='split'),
    })

def backTest(request,code='000001', start='2014-01-01', end='2016-01-01'):
    code = request.GET.get('code')
    start = request.GET.get('start')
    end = request.GET.get('end')

    standard_bars = tushare.get_hist_data("hs300",start=start, end=end).sort_index()
    standard_bars['close'][:] = (standard_bars['close'][:] - standard_bars['open'][0])/standard_bars['open'][0]
    bars = tushare.get_hist_data(code,start=start, end=end).sort_index()
    

    test_strategy = MAStrategy(bars)
    signals = test_strategy.gen_signal()
    test_trade = MATrade(bars,signals)
    capital = test_trade.trade_tracing() 
    return HttpResponse(json.dumps({
            'dateData': capital['yieldRate'].to_json(orient='split'),
            'yieldRateData': capital['yieldRate'].to_json(orient='split'),
            'standardData': standard_bars['close'].to_json(orient='split'),
    }),content_type="application/json")
