import pandas as pd
from stockIndex import StockIndex
import numpy as np
from sklearn import svm
from quanter.stockdata import *
from quanter.svm import *
import pickle
import os

class Strategy(object):
    def __init__(self):
        pass

    def gen_signal(self):
        pass

    def get_stockIndex(self,close = None, open = None, high = None, low = None, volume = None):
        st = StockIndex(close,open,high,low,volume)
        return st


class MAStrategy(Strategy):
    def __init__(self,short_window=5, long_window=20):
        self.short_window = short_window
        self.long_window = long_window

    def gen_signal(self,bar):
        st = super(MAStrategy, self).get_stockIndex(bar['close'])
        # signal = pd.Series(index = bar.index)
        sma = st.MA(windows=self.short_window)
        lma = st.MA(windows=self.long_window)
        flag = np.where(sma>lma,1,-1)
        signal = pd.Series(flag,index = bar.index)
        return signal

class BIASStrategy(Strategy):
    def __init__(self,n=10):
        self.n = n

    def gen_signal(self,bar):
        st = super(BIASStrategy, self).get_stockIndex(bar['close'])
        bias = st.BIAS(n=self.n)
        print bias
        flag = np.where(bias>8,-1,0)
        flag = np.where(bias<-8,1,flag)
        signal = pd.Series(flag,index = bar.index)
        return signal

class WRStrategy(Strategy):
    def __init__(self,n=14):
        self.n = n

    def gen_signal(self,bar):
        st = super(WRStrategy, self).get_stockIndex(bar['close'])
        # signal = pd.Series(index = bar.index)
        wr = st.WR(N=self.n)
        flag = np.where(wr>80,1,0)
        flag = np.where(wr<20,-1,flag)
        signal = pd.Series(flag,index = bar.index)
        return signal

class SVMStrategy(Strategy):
    def __init__(self,clName = None,code=None,start=None,end=None):
        self.clName = clName
        self.code = code
        self.start = start 
        self.end = end

    def cal_clf(self):
        if os.path.exists('cl/'+self.clName):
            print self.clName+"exist"
            f = open('cl/'+self.clName,'rb')
            cl = pickle.load(f)
            return cl
        service = StockDataFactory().getStockDataService()
        df = service.getStockData(self.code,start = self.start,end=self.end)
        st = StockIndex(df["close"],df["open"],df["high"],df["low"],df["volume"])
        x = st.getNeedData()
        x = x[10:]
        x = x/100
        y = df['close'].diff()>0
        y = y*2-1
        y = y[10:]
        g = GridSearch()
        cl = g.getClassifier(x[:-1],y[1:])
        f = open('cl/'+self.clName,'wb')
        pickle.dump(cl,f)
        f.close()
        return cl
        
    def get_clf(self):
        f = open('cl/'+self.clName,'rb')
        cl = pickle.load(f)
        return cl

    def gen_signal(self,bar):
        st = super(SVMStrategy, self).get_stockIndex(bar['close'],bar['open'],bar['high'],bar['low'])
        bar = bar[10:]
        df = st.getNeedData()
        df = df[10:]
        df = df/100
        y = bar['close'].diff()>0
        y = y*2-1

        # clf = svm.SVC()
        # trainNum = int(float(self.trainRatio) * len(df))
        # clf.fit(df[:trainNum], y[1:trainNum+1])
        # yResult = clf.predict(df[trainNum:])
        if self.code is None:
            clf = self.get_clf()
        else:
            clf = self.cal_clf()
        yResult = clf.predict(df)

        signal = pd.Series(yResult,index = bar.index)
        return signal

class CustomStrategy(Strategy):
    def __init__(self,buyStr,sellStr):
        self.buyStr = self.dealStr(buyStr)
        self.sellStr = self.dealStr(sellStr)

    def dealStr(self,string):
        string = string.replace('close',"bar['close']")
        string = string.replace('open',"bar['open']")
        string = string.replace('high',"bar['high']")
        string = string.replace('low',"bar['low']")
        string = string.replace('MA(',"st.MA(windows=")
        string = string.replace('BIAS(',"st.BIAS(n=")
        string = string.replace('PSY(',"st.PSY(n=")
        string = string.replace('RSI(',"st.RSI(N=")
        string = string.replace('WR(',"st.WR(N=")
        print string
        return string

    def gen_signal(self,bar):
        st = super(CustomStrategy, self).get_stockIndex(bar['close'],bar['open'],bar['high'],bar['low'])
        # signal = pd.Series(index = bar.index)
        buy = eval(self.buyStr)
        sell = eval(self.sellStr)
        flag = np.where(buy,1,0)
        flag = np.where(sell,-1,flag)
        signal = pd.Series(flag,index = bar.index)
        return signal