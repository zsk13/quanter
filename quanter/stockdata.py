import tushare as ts
import time
from quanter.models import *
from datetime import datetime
import pandas as pd

class StockDataFactory(object):
    @classmethod
    def getStockDataService(cls):
        return StockDataServiceDatabaseImpl()

    @classmethod
    def getStockDataServiceByStartTime(cls,start):
        if start>"2014-01-01":
            return StockDataServiceDatabaseImpl()
        else:
            return StockDataServiceTSImpl()

class StockDataService(object):
    def getStockData(self,code,start = None,end =None,index = False):
        pass

    def getStockDataAsObject(self, code, start = None, end=None,index = False):
        pass

class StockDataServiceTSImpl(StockDataService):
    def getStockData(self,code,start = None,end =None,index = False):
        df = ts.get_h_data(code = code,start = start, end = end, index = index).sort_index()
        return df



class StockDataServiceDatabaseImpl(StockDataService):
    def getStockData(self,code,start = None,end =None,index = False):
        stock = Stock.objects.get(code=code)
        if start is None and end is None:
            df = pd.DataFrame(list(stock.daydata_set.all().values("date","open","close","high","low","volume","amt")))
        else:
            start = datetime.strptime(start, "%Y-%m-%d")
            end = datetime.strptime(end, "%Y-%m-%d")
            df = pd.DataFrame(list(stock.daydata_set.filter(date__gte=start).filter(date__lte=end).values("date","open","close","high","low","volume","amt")))

        if len(df)==0:
            return df
        df = df.set_index("date")
        df = df.sort_index()
        return df

    def getStockDataAsObject(self, code, start = None, end=None,index = False):
        stock = Stock.objects.get(code=code)
        if start is None and end is None:
            dayDatas = stock.daydata_set.order_by('date')
        else:
            start = datetime.strptime(start, "%Y-%m-%d")
            end = datetime.strptime(start, "%Y-%m-%d")
            dayDatas = stock.dayData_set.filter(date__gte=start).filter(date__lte=end).order_by('date')
        
        return dayDatas