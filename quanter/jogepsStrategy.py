# encoding: UTF-8
from quanter.models import Stock,DayData,MAData,ProfitRateData
import datetime
from quanter.formStrategy import Helper,FormStrategy

class JogepsStrategy(FormStrategy):
    def __init__(self,type):
        super(JogepsStrategy, self).__init__(type)

    def getRecommendPara(self):
        paraList = {'short':10,'long':20}
        return paraList

class JogepsHelper(Helper):
    def __init__(self,paraList):
        self.short = paraList['short']
        self.long = paraList['long']

    def levelOfBuy(self,date,index):
        res = []
        yesterday = self.getDateBefore(date,1)
        dataList = []
        for i in range(0,2):
            dataList.append({'daydata':self.dayData.get(date = self.getDateBefore(date,i)),
                             'madata':self.maData.get(date = self.getDateBefore(date,i))})

        if index >10 and self.isMADescendingToFlat(yesterday) and self.rateMA(date) > 0 and self.isUpperMA(date):
            level = 2+self.levelOfVolume(date,index)
            res.append(level)
        if index >10 and self.isCloseDescending(yesterday) and self.isAboveMA(yesterday) and self.rateClose(date) >0:
            level = 2+self.levelOfVolume(date,index)
            res.append(level)
        if index >10 and self.isCloseDescending(date) and self.isAboveMA(yesterday) and \
                        dataList[0]['daydata'].close <dataList[0]['madata'].ma10 and self.rateMA(date)>0:
            level = 2+self.levelOfVolume(date,index)
            res.append(level)
        if index >10 and self.isMARising(date) and self.isMARising(date) and dataList[0]['madata'].ma10 >=dataList[0]['madata'].ma20\
            and dataList[1]['madata'].ma10 <= dataList[1]['madata'].ma20:
            level = 1+self.levelOfVolume(date,index)
            res.append(level)

        res.append(0)
        return res

    def levelOfSale(self,date,index):
        yesterday = self.getDateBefore(date,1)
        dataList = []
        for i in range(0,2):
            dataList.append({'daydata':self.dayData.get(date = self.getDateBefore(date,i)),
                             'madata':self.maData.get(date = self.getDateBefore(date,i))})

        if index >10 and self.isMARisingToFlat(date) and self.isLowerMA(date):
            level = 2 +self.levelOfVolume(date,index)
            return level
        if index >10 and self.isBelowMA(date) and self.isCloseRising(date) and \
                dataList[0]['daydata'].close <dataList[0]['madata'].ma10 and \
            self.isMARisingToFlat(yesterday) and self.rateMA(date) >self.rateMA(yesterday):
            level = 2+self.levelOfVolume(date,index)
            return level
        if index >10 and self.isAboveMA(date) and self.isCloseDescending(date) and \
            dataList[0]['daydata'].close <dataList[0]['madata'].ma10 and self.rateMA(date) <0:
            level = 2+self.levelOfVolume(date,index)
            return level
        if index >10 and self.isMADescending(date) and dataList[0]['madata'].ma10 <=dataList[0]['madata'].ma20\
            and dataList[1]['madata'].ma10 >= dataList[1]['madata'].ma20:
            level = 1+self.levelOfVolume(date,index)
            return level

        return 0

    def isMADescendingToFlat(self,date):
        for i in range(0,10):
            yesterday = self.getDateBefore(date,1)
            if self.rateMA(date) <0 and self.rateMA(date) >self.rateMA(yesterday) :
                date = yesterday
                continue
            else:
                return 0

        return 1

    def isMARisingToFlat(self,date):
        for i in range(0,10):
            yesterday = self.getDateBefore(date,1)
            if self.rateMA(date) >0 and self.rateMA(date) <self.rateMA(yesterday) :
                date = yesterday
                continue
            else:
                return 0

        return 1

    def isMARising(self,date):
        for i in range(0,10):
            yesterday = self.getDateBefore(date,1)
            if self.rateMA(date) >0 and self.rateMALong(date) >0:
                date = yesterday
                continue
            else:
                return 0

        return 1

    def isMADescending(self,date):
        for i in range(0,10):
            yesterday = self.getDateBefore(date,1)
            if self.rateMA(date) <0 and self.rateMALong(date) <0:
                date = yesterday
                continue
            else:
                return 0

        return 1

    def isCloseDescending(self,date):
        for i in range(0,10):
            yesterday = self.getDateBefore(date,1)
            if self.rateClose(date) <0 :
                date = yesterday
                continue
            else:
                return 0

        return 1

    def isCloseRising(self,date):
        for i in range(0,10):
            yesterday = self.getDateBefore(date,1)
            if self.rateClose(date) >0 :
                date = yesterday
                continue
            else:
                return 0

        return 1

    def rateMA(self,date):
        return (self.maData.get(date = date).ma10 - self.maData.get(date = self.getDateBefore(date,1)).ma10 ) / self.maData.get(date = self.getDateBefore(date,1)).ma10

    def rateMALong(self,date):
        return (self.maData.get(date = date).ma20 - self.maData.get(date = self.getDateBefore(date,1)).ma20 ) / self.maData.get(date = self.getDateBefore(date,1)).ma20

    def rateClose(self,date):
        return (self.dayData.get(date = date).close - self.dayData.get(date = self.getDateBefore(date,1)).close ) / self.dayData.get(date = self.getDateBefore(date,1)).close

    def isUpperMA(self,date):
        yesterday = self.getDateBefore(date,1)
        if self.dayData.get(date = yesterday).close <= self.maData.get(date = yesterday).ma10 and self.dayData.get(date = date).close >= self.maData.get(date = date).ma10:
            return 1
        else:
            return 0

    def isLowerMA(self,date):
        yesterday = self.getDateBefore(date,1)
        if self.dayData.get(date = yesterday).close >= self.maData.get(date = yesterday).ma10 and self.dayData.get(date = date).close <= self.maData.get(date = date).ma10:
            return 1
        else:
            return 0

    def isAboveMA(self,date):
        for i in range(0,10):
            yesterday = self.getDateBefore(date,1)
            if self.dayData.get(date = date).close >= self.maData.get(date = date).ma10 :
                date = yesterday
                continue
            else:
                return 0

        return 1

    def isBelowMA(self,date):
        for i in range(0,10):
            yesterday = self.getDateBefore(date,1)
            if self.dayData.get(date = date).close <= self.maData.get(date = date).ma10 :
                date = yesterday
                continue
            else:
                return 0

        return 1





