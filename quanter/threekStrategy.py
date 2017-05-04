# encoding: UTF-8
from quanter.models import Stock,DayData,MAData,ProfitRateData
import datetime
from quanter.formStrategy import Helper,FormStrategy

class ThreekStrategy(FormStrategy):
    def __init__(self,type):
        super(ThreekStrategy, self).__init__(type)

    def getRecommendPara(self):
        paraList = {'long':0.036,'short':0.15,'mid':0.035,'mini':0.005}
        return paraList

class KLineHelper(Helper):
    def __init__(self,paraList):
        self.long=paraList['long']
        self.mid=paraList['mid']
        self.short=paraList['short']
        self.mini=paraList['mini']

#   给出当天的买入推荐等级 -1代表异常 0代表不推荐  数字越大代表推荐程度越高 范围为1-5
    def levelOfBuy(self,date,index):
        res=[]
        level=0

        #date=self.getIndexOfDate(date)
        yesterday = self.getDateBefore(date,1)
        theDayBeforeYesterday = self.getDateBefore(date,2)
        dataList = []
        for i in range(0,3):
            dataList.append({'daydata':self.dayData.get(date = self.getDateBefore(date,i))})

#        穿刺线
        if index>0 and self.isDescending(yesterday,index-1) and self.isLower(yesterday) \
                and self.rate(yesterday)>self.long and self.isUpper(date) and \
                self.isUpperMiddle(date) and dataList[0]['daydata'].open<dataList[1]['daydata'].close and \
                self.isHighVolume(date,index):
            level=1
            level=level+self.levelOfVolume(date,index)
            res.append(level)
            res.append(1)
            return res
#        早晨之星
        if index>1 and self.isDescending(theDayBeforeYesterday,index-1) and self.isLower(theDayBeforeYesterday) and \
                        self.rate(theDayBeforeYesterday)>self.long and self.rate(yesterday)<self.short and \
                        dataList[1]['daydata'].close<dataList[2]['daydata'].close and self.isUpper(date) and \
                        self.rate(date)>self.long and dataList[0]['daydata'].open>dataList[1]['daydata'].open and \
                        dataList[0]['daydata'].open>dataList[1]['daydata'].close and self.isHighVolume(date,index) and \
                self.isShortUS(date):
            res.append(3)
            res.append(2)
            return res
#        孕育行
        if index>0 and self.isDescending(yesterday,index-1) and self.isLower(yesterday) and \
                        self.rate(yesterday)>self.short and self.rate(date)<self.short and \
                        dataList[0]['daydata'].open<dataList[1]['daydata'].open and \
                        dataList[0]['daydata'].open>dataList[1]['daydata'].close and \
                        dataList[0]['daydata'].close<dataList[1]['daydata'].open and \
                        dataList[0]['daydata'].open>dataList[1]['daydata'].close and self.isHighVolume(date,index) and \
                self.isShortLS(yesterday):
            level=1+self.levelOfVolume(date,index)
            res.append(level)
            res.append(3)
            return res
#       穿头破脚
        if index>1 and self.isDescending(yesterday,index-1) and self.isLower(yesterday) and \
                        self.rate(yesterday)<self.short and self.isUpper(date) and \
                        dataList[1]['daydata'].open<dataList[0]['daydata'].close and \
                        dataList[1]['daydata'].open>dataList[0]['daydata'].open and \
                        dataList[1]['daydata'].close<dataList[0]['daydata'].close and \
                        dataList[1]['daydata'].open>dataList[0]['daydata'].open and \
                        self.rate(date)>self.short and self.isHighVolume(date,index):

            level=2+self.levelOfVolume(date,index)
            res.append(level)
            res.append(4)
            return res
#        红三兵
        if index>1 and (self.isDescending(theDayBeforeYesterday,index-2) or self.isTransverse(theDayBeforeYesterday)) and \
                self.isUpper(theDayBeforeYesterday) and self.isUpper(yesterday) and self.isUpper(date) and \
                        dataList[1]['daydata'].open>(dataList[2]['daydata'].open+dataList[2]['daydata'].close)/2 and \
                        dataList[0]['daydata'].open>(dataList[1]['daydata'].open+dataList[1]['daydata'].close)/2 and \
                        self.rate(theDayBeforeYesterday)>self.long and self.rate(yesterday)>self.long and \
                        self.rate(date)>self.long and self.isHighVolume(date,index) and self.isHighVolume(yesterday,index-1):
            level=4+self.levelOfVolume(date,index)
            res.append(level)
            res.append(5)
            return res
#        锤形线
        if index>0 and self.isDescending(yesterday,index-1) and self.hasBreach(yesterday) and \
                        self.rate(yesterday)<self.mid and \
                ((dataList[1]['daydata'].open>dataList[1]['daydata'].close and \
                              (dataList[1]['daydata'].open-dataList[1]['daydata'].close)\
                                  <0.33*(dataList[1]['daydata'].close-dataList[1]['daydata'].low)) or \
                         (dataList[1]['daydata'].close>dataList[1]['daydata'].open and \
                                      (dataList[1]['daydata'].close-dataList[1]['daydata'].open)<\
                                              0.33*(dataList[1]['daydata'].open-dataList[1]['daydata'].low))) and \
                self.isShortUS(yesterday) and self.isHighVolume(yesterday,index-1) and self.isUpper(date) and \
                        dataList[0]['daydata'].close>dataList[1]['daydata'].close and self.isHighVolume(date,index):
            level=2
            level=level+self.levelOfVolume(date,index)
            res.append(level)
            res.append(6)
            return res
#        倒锤形
        if index>0 and self.isDescending(yesterday,index-1) and self.rate(yesterday)<self.mid and \
                ((dataList[1]['daydata'].close>dataList[1]['daydata'].open and \
                              (dataList[1]['daydata'].close-dataList[1]['daydata'].open)<\
                                      0.33*(dataList[1]['daydata'].high-dataList[1]['daydata'].close)) or \
                         (dataList[1]['daydata'].open>dataList[1]['daydata'].close and \
                                  ((dataList[1]['daydata'].open-dataList[1]['daydata'].close)<\
                                               0.33*(dataList[1]['daydata'].low-dataList[1]['daydata'].open)))) and \
                self.isShortLS(yesterday) and dataList[0]['daydata'].open>dataList[1]['daydata'].open and \
                        dataList[0]['daydata'].open>dataList[1]['daydata'].close and \
                self.isUpper(date) and self.isHighVolume(date,index):
            level=2+self.levelOfVolume(date,index)
            res.append(level)
            res.append(7)
            return res
        #       长十字线
        if (self.isDescending(date,index) or self.isTransverse(date)) and self.rate(date)<self.mini and self.isHighVolume(date,index):
            if dataList[0]['daydata'].open>dataList[0]['daydata'].close and \
                                    (dataList[0]['daydata'].high-dataList[0]['daydata'].open)/dataList[0]['daydata'].open>self.short and \
                                    (dataList[0]['daydata'].close-dataList[0]['daydata'].low)/dataList[0]['daydata'].close>self.short:
                level=1+self.levelOfVolume(date,index)
                res.append(level)
                res.append(8)
                return res
            if dataList[0]['daydata'].open<dataList[0]['daydata'].close and \
                                    (dataList[0]['daydata'].high-dataList[0]['daydata'].close)/dataList[0]['daydata'].close>self.short and \
                                    (dataList[0]['daydata'].open-dataList[0]['daydata'].low)/dataList[0]['daydata'].open>self.short:
                level=1+self.levelOfVolume(date,index)
                res.append(level)
                res.append(8)
                return res
        res.append(0)
        res.append(-1)
        return res

#   给出当天的卖出的推荐等级 -1代表异常 0代表不推荐 数字越大代表推荐程度越高 范围为1-5
    def levelOfSale(self,date,index):
        #date=self.getIndexOfDate(date)
        level=0
        yesterday = self.getDateBefore(date,1)
        theDayBeforeYesterday = self.getDateBefore(date,2)
        twoDaysBeforeYesterday = self.getDateBefore(date,3)
        dataList = []
        for i in range(0,4):
            dataList.append({'daydata':self.dayData.get(date = self.getDateBefore(date,i))})

#    乌云压顶
        if index>0 and self.isRising(yesterday,index-1) and self.isUpper(yesterday) and \
                        self.rate(yesterday)>=self.long  and self.isLower(date) and \
                self.isLowerMiddle(date) and self.isHighVolume(date,index):
            level=1
            level=level+self.levelOfVolume(date,index)
            return level
#        黄昏之星
        if index>1 and self.isRising(theDayBeforeYesterday,index-2) and self.isUpper(theDayBeforeYesterday) and \
                        self.rate(theDayBeforeYesterday)>self.long and self.rate(yesterday)<self.short and \
                self.hasBreach(yesterday) and self.isLower(date) and \
                ((self.isUpper(yesterday) and dataList[0]['daydata'].open<dataList[1]['daydata'].open) or (self.isLower(yesterday) and dataList[0]['daydata'].open<dataList[1]['daydata'].close)) and \
                        self.rate(date)>self.long and(self.isHighVolume(date,index) or self.isHighVolume(yesterday,index-1)):
            return 3
#        孕育行
        if index>0 and self.isRising(yesterday,index-1) and self.isUpper(yesterday) and self.rate(yesterday)>self.short and \
                        self.rate(date)<self.short and dataList[0]['daydata'].open>dataList[1]['daydata'].open and \
                        dataList[0]['daydata'].open<dataList[1]['daydata'].close and dataList[0]['daydata'].close>dataList[1]['daydata'].open and \
                        dataList[0]['daydata'].open<dataList[1]['daydata'].close and self.isHighVolume(date,index) and \
                self.isShortLS(yesterday):
            return 1
#        穿头破脚
        if index>0 and self.isRising(yesterday,index-1) and self.isUpper(yesterday) and self.rate(yesterday)<self.short and \
                        self.rate(yesterday)>self.mini and self.isLower(date) and \
                        dataList[1]['daydata'].open<dataList[0]['daydata'].open and \
                        dataList[1]['daydata'].open>dataList[0]['daydata'].close and \
                        dataList[1]['daydata'].close<dataList[0]['daydata'].open and \
                        dataList[1]['daydata'].open>dataList[0]['daydata'].close and self.isHighVolume(date,index):
            level=2+self.levelOfVolume(date,index)
            return level
#        强弩之末
        if index>1 and self.isRising(theDayBeforeYesterday,index-2) and self.isUpper(theDayBeforeYesterday) and \
                self.isUpper(yesterday) and self.isRising(theDayBeforeYesterday,index-2) and \
                        self.rate(theDayBeforeYesterday)>self.long and self.rate(yesterday)>self.long and \
                        self.rate(date)<self.mini and dataList[1]['daydata'].close>dataList[2]['daydata'].close and \
                        dataList[0]['daydata'].close>dataList[1]['daydata'].close and self.isHighVolume(date,index) and \
                self.isHighVolume(yesterday,index-1):
            level=2+self.levelOfVolume(date,index)
            return level
#        三乌鸦
        if index>1 and self.isRising(theDayBeforeYesterday,index-2) and self.isLower(theDayBeforeYesterday) and \
                self.isLower(yesterday) and self.isLower(date) and self.rate(theDayBeforeYesterday)>self.short and \
                        self.rate(yesterday)>self.short and self.rate(date)>self.short and \
                        dataList[0]['daydata'].close<dataList[1]['daydata'].close and \
                        dataList[1]['daydata'].close<dataList[2]['daydata'].close and \
                        dataList[1]['daydata'].open>dataList[2]['daydata'].close and \
                        dataList[0]['daydata'].open>dataList[1]['daydata'].close:
            level=4+self.levelOfVolume(yesterday,index-1)
            return level
#        上升缺口两乌鸦
        if index>1 and self.isRising(theDayBeforeYesterday,index-2) and self.isUpper(theDayBeforeYesterday) and \
                        self.rate(theDayBeforeYesterday)>self.long and self.isLower(yesterday) and \
                self.hasBreach(yesterday) and self.isLower(date) and \
                        dataList[0]['daydata'].close<dataList[1]['daydata'].close and self.isHighVolume(date,index):
            level=3+self.levelOfVolume(date,index)
            return level
#        射击之星
        if  index>0 and self.isRising(yesterday,index-1) and self.rate(yesterday)<self.short and \
                self.isHighVolume(date,index) and \
                ((dataList[0]['daydata'].close>dataList[0]['daydata'].open and ((dataList[0]['daydata'].close-dataList[0]['daydata'].open)<0.33*(dataList[0]['daydata'].high-dataList[0]['daydata'].close))) or \
                         ((dataList[0]['daydata'].open>dataList[0]['daydata'].close and (dataList[0]['daydata'].open-dataList[0]['daydata'].close)<0.33*(dataList[0]['daydata'].high-dataList[0]['daydata'].open)))) and \
                self.isShortLS(date):
            level=2
            level=level+self.levelOfVolume(yesterday,index-1)
            return level
#        上吊线
        if self.isRising(date,index) and self.rate(date)<self.mid and  self.hasBreach(date) and \
                ((dataList[0]['daydata'].close>dataList[0]['daydata'].open and ((dataList[0]['daydata'].close-dataList[0]['daydata'].open)<0.5*(dataList[0]['daydata'].open-dataList[0]['daydata'].low))) or \
                         (dataList[0]['daydata'].open>dataList[0]['daydata'].close and ((dataList[0]['daydata'].open-dataList[0]['daydata'].close)<0.5*(dataList[0]['daydata'].close-dataList[0]['daydata'].low)))) and \
                self.isShortUS(date) and self.isHighVolume(date,index):
            level=1+self.levelOfVolume(date,index)
            return level
#       长十字线
        if self.isRising(date,index) and self.rate(date)<self.short and self.isHighVolume(date,index):
            if dataList[0]['daydata'].open>dataList[0]['daydata'].close and (dataList[0]['daydata'].high-dataList[0]['daydata'].open)/dataList[0]['daydata'].open>self.short and (dataList[0]['daydata'].close-dataList[0]['daydata'].low)/dataList[0]['daydata'].close>self.short:
                level=1+self.levelOfVolume(date,index)
                return level
            if dataList[0]['daydata'].open<dataList[0]['daydata'].close and (dataList[0]['daydata'].high-dataList[0]['daydata'].close)/dataList[0]['daydata'].close>self.short and (dataList[0]['daydata'].open-dataList[0]['daydata'].low)/dataList[0]['daydata'].open>self.short:
                level=1+self.levelOfVolume(date,index)
                return level
#        淡友反攻
        if index>0 and self.isRising(yesterday,index-1) and self.isUpper(yesterday) and self.rate(yesterday)>=self.mid  and \
                self.isLower(date) and self.rate(date)>self.mid and \
                        abs((dataList[0]['daydata'].close-dataList[1]['daydata'].close)/dataList[1]['daydata'].close)<self.short and self.isHighVolume(date,index):
            level=1+self.levelOfVolume(date,index)
            return level
#        倾盆大雨
        if index>0 and self.isRising(yesterday,index-1) and self.isUpper(yesterday) and self.rate(yesterday)>=self.mid and \
                self.isLower(date) and self.rate(date)>=self.mid and \
                        dataList[0]['daydata'].open<dataList[1]['daydata'].close and self.isHighVolume(date,index):
            level=1+self.levelOfVolume(date,index)
            return level
#        下跌三颗星
        if index>2 and self.isRising(twoDaysBeforeYesterday,index-3) and self.isLower(twoDaysBeforeYesterday) and \
                        self.rate(twoDaysBeforeYesterday)>self.mid and self.rate(theDayBeforeYesterday)<0.02 and \
                        self.rate(yesterday)<0.02 and self.rate(date)<0.02 and \
                        abs((dataList[2]['daydata'].close-dataList[3]['daydata'].close)/dataList[3]['daydata'].close)<0.02 and abs((dataList[1]['daydata'].close-dataList[3]['daydata'].close)/dataList[3]['daydata'].close)<0.02 and \
                        abs((dataList[0]['daydata'].close-dataList[3]['daydata'].close)/dataList[3]['daydata'].close)<0.02:
            level=2
            return level
        return 0



