from quanter.strategy import *
from quanter.trade import *
from quanter.stockdata import *
import json
import datetime

class BackTest(object):
    def __init__(self,code,start,end,strategy = MAStrategy(), init_capital = 100000.0,benchmark = '399300'):
        self.dataService = StockDataFactory.getStockDataServiceByStartTime(start)
        self.df = self.dataService.getStockData(code,start = start,end = end)
        self.trade = Trade(self.df,strategy = strategy, init_capital = init_capital)
        self.benchmark = benchmark        

    def setStrategy(self,strategy):
        self.trade.setStrategy(strategy)

    def formatTimeStamp(self, time):
        dt = datetime.datetime(time.year,time.month,time.day)
        string = dt.strftime("%Y-%m-%d")
        return string

    def getJsonResult(self):
        capital = self.trade.trade_tracing()
        starttime = self.formatTimeStamp(capital.index[0])
        endtime = self.formatTimeStamp(capital.index[-1])
        self.standardDf = self.dataService.getStockData(self.benchmark,start = starttime,end = endtime, index = True)
        standard_bars = (self.standardDf['close'] - self.standardDf['open'][0])/self.standardDf['open'][0]

        jsonData = json.dumps({
            'dateData': capital['yieldRate'].to_json(orient='split'),
            'yieldRateData': capital['yieldRate'].to_json(orient='split'),
            'standardData': standard_bars.to_json(orient='split'),
        })
        return jsonData

    def getSimpleResult(self):
        rate = self.trade.getSuccessRate()
        return rate