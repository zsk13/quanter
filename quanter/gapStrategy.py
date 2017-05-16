# encoding: UTF-8
from quanter.models import Stock,DayData,MAData,ProfitRateData
import datetime
from quanter.formStrategy import Helper,FormStrategy

class GapStrategy(FormStrategy):
    def __init__(self,type):
        super(GapStrategy, self).__init__(type)

    def getRecommendPara(self):
        paraList = {'breach':0.0001}
        return paraList

class GapHelper(Helper):
    def __init__(self,paraList):
        self.breach = float(paraList['breach'])

    def levelOfBuy(self,date,index):
        res = []
        yesterday = self.getDateBefore(date,1)
        dataList = []
        for i in range(0,2):
            dataList.append({'daydata':self.dayData.get(date = self.getDateBefore(date,i)),
                             'madata':self.maData.get(date = self.getDateBefore(date,i))})

        if index >1 and self.hasUpBreach(yesterday) and self.isHighVolume(yesterday,index-1) and \
                        dataList[0]['daydata'].volume >dataList[1]['daydata'].volume:
            level = 2 +self.levelOfVolume(date,index)
            res.append(level)

        if index >1 and self.hasUpBreach(yesterday) and min(dataList[0]['daydata'].close,dataList[0]['daydata'].open) > dataList[0]['madata'].ma20\
            and max(dataList[1]['daydata'].close,dataList[1]['daydata'].open) < dataList[0]['madata'].ma20:
            level = 1 +self.levelOfVolume(date,index)
            res.append(level)

        if index >40 and self.hasThirdDownBreach(date) :
            level = 1+self.levelOfVolume(date,index)
            res.append(level)
        

        res.append(0)
        return res

    def levelOfSale(self,date,index):
        res = []
        yesterday = self.getDateBefore(date,1)
        dataList = []
        for i in range(0,2):
            dataList.append({'daydata':self.dayData.get(date = self.getDateBefore(date,i)),
                             'madata':self.maData.get(date = self.getDateBefore(date,i))})

        if index >1 and self.hasDownBreach(yesterday) and min(dataList[0]['daydata'].close,dataList[0]['daydata'].open) < dataList[0]['madata'].ma20\
            and max(dataList[1]['daydata'].close,dataList[1]['daydata'].open) > dataList[0]['madata'].ma20:
            level = 1 +self.levelOfVolume(date,index)
            return level
        if index >40 and self.hasThirdUpBreach(date) :
            level = 1 +self.levelOfVolume(date,index)
            return level

        return 0



    def hasUpBreach(self,date):
        dataList = []
        for i in range(0,2):
            dataList.append({'daydata':self.dayData.get(date = self.getDateBefore(date,i))})


        if (dataList[0]['daydata'].low - dataList[1]['daydata'].high )/ dataList[1]['daydata'].high > self.breach:
            return 1
        return 0

    def hasDownBreach(self,date):
        dataList = []
        for i in range(0,2):
            dataList.append({'daydata':self.dayData.get(date = self.getDateBefore(date,i))})

        if (dataList[0]['daydata'].high - dataList[1]['daydata'].low )/ dataList[1]['daydata'].low < -self.breach:
            return 1
        return 0

    def hasThirdUpBreach(self,date):
        upBreach_num = 0
        for i in range(0,40):
            cur_date = self.getDateBefore(date,39-i)
            if self.hasUpBreach(cur_date):
                upBreach_num += 1
                if upBreach_num ==3 and cur_date == date:
                    return 1

            if self.hasDownBreach(cur_date):
                upBreach_num = 0

        return 0

    def hasThirdDownBreach(self,date):
        downBreach_num = 0
        for i in range(0,40):
            cur_date = self.getDateBefore(date,39-i)
            if self.hasDownBreach(cur_date):
                downBreach_num += 1
                if downBreach_num ==3 and cur_date == date:
                    return 1

            if self.hasUpBreach(cur_date):
                downBreach_num = 0

        return 0



