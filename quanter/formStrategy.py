# encoding: UTF-8
from quanter.models import Stock,DayData,MAData,ProfitRateData
import datetime

class FormStrategy(object):
    def __init__(self,type):
        self.type = type

    def getRecommendPara(self):
        pass

    def getRecommendStock(self):
        stocks_recommend = ProfitRateData.objects.filter(strategy = self.type).order_by('-profitRate')[0:9]
        return stocks_recommend

    def setPara(self,start,end,iniMoney):
        self.line = -0.08
        self.start = start
        self.end = end
        self.initial_money = iniMoney

    def setHelper(self,helper):
        self.helper = helper

    def autobuy(self,codeArea):
        profitRate_day = []
        startDate = datetime.datetime.strptime(self.start,"%Y-%m-%d").date()
        endDate = datetime.datetime.strptime(self.end,"%Y-%m-%d").date()
        money = float(self.initial_money)
        st_example = Stock.objects.filter(isInPool = 1).first()
        dates_example = DayData.objects.filter(stock= st_example,date__range =(startDate,endDate))
        trade_dates = dates_example.values("date")[5:]
        # 取数据
        stock_dayDatas = {}
        stock_maDatas = {}

        for cd in codeArea:
            st = Stock.objects.get(code = cd)
            stock_dayDatas[cd] = DayData.objects.filter(stock = st, date__range =(startDate,endDate))
            stock_maDatas[cd] = MAData.objects.filter(stock = st, date__range =(startDate,endDate))


        #自动交易
        trade_record = []
        stocks_hold = []
        line = self.line

        index_date = 5
        for date in trade_dates:
            date = date['date']
            orders_buy = []

            #查看卖讯号
            for st in stocks_hold:
                day_data = stock_dayDatas[st['code']].get(date = date)
                self.helper.setData(stock_dayDatas[st['code']],stock_maDatas[st['code']])
                levelOfSale = self.helper.levelOfSale(date,index_date)

                #符合卖出形态
                #最低价跌过警戒线
                #回测最后一天全部卖出
                if levelOfSale >= 1 or float(day_data.low - st['price']) / st['price'] < line or date == dates_example.order_by('-date')[0].date:
                    trade_record.append({'date':date,'st_code':st['code'],'trade_type':'sale','number':st['number'],'price':day_data.close,'total':st['number']*day_data.close})
                    money += st['number']* day_data.close
                    stocks_hold.remove(st)


            #查看买讯号
            for cd in codeArea:
                day_data = stock_dayDatas[cd].get(date = date)
                self.helper.setData(stock_dayDatas[cd],stock_maDatas[cd])
                levelOfBuy = self.helper.levelOfBuy(date,index_date)
                if levelOfBuy[0] >= 1:
                    orders_buy.append({'st_code':cd,'price':day_data.open,'level':levelOfBuy[0]})

            #根据推荐等级进行降序排序
            orders_buy.sort(key= lambda order:order['level'], reverse= True)

            for order in orders_buy:
                if money < order['price']:
                    continue
                number = int(money/order['price'])
                money -= order['price']*number
                trade_record.append({'date':date,'st_code':order['st_code'],'trade_type':'buy',
                                     'number':number,'price':order['price'],'total':number*order['price']})
                stocks_hold.append({'code':order['st_code'],'price':order['price'],'number':number})

            index_date += 1
            #计算目前持有股票的现值
            current_stockValue = 0
            for st in stocks_hold:
                day_data = stock_dayDatas[st['code']].get(date = date)
                current_stockValue += day_data.close*st['number']

            current_totalValue = current_stockValue +money

            profitRate_day.append([str(date),current_totalValue])

        #return profitRate_day
        #return (money- self.initial_money)/self.initial_money*100
        #return trade_record
        result = {'profitRate':(money- self.initial_money)/self.initial_money*100,'profitRate_day':profitRate_day,'trade_record':trade_record}
        return result

    def storeRecommendStock(self,start,end):
        self.line = -0.08
        self.start = start
        self.end = end
        self.initial_money = 1000000.0


        stockList = Stock.objects.filter(isInPool = 1)[1:10]


        for stock in stockList:
            codeArea = [stock.code]

            profit_rate = self.autobuy(codeArea)['profitRate']
            profitRateData = ProfitRateData()
            profitRateData.stock = stock
            profitRateData.year = int(start[0:4])
            profitRateData.profitRate = profit_rate
            profitRateData.strategy = self.type
            profitRateData.save()

    def getTradeRecord(self,start,end):
        self.line = -0.08
        self.start = start
        self.end = end
        self.initial_money = 1000000.0
        codeArea = ['SH600012']
        trade_record = self.autobuy(codeArea)['trade_record']
        return trade_record

class Helper(object):
    def __init__(self):
        pass
    def setData(self,dayData,maData):
        self.dayData= dayData
        self.maData = maData


#   给出当天的买入推荐等级 -1代表异常 0代表不推荐  数字越大代表推荐程度越高 范围为1-5
    def levelOfBuy(self,date,index):
        pass
    #   给出当天的卖出的推荐等级 -1代表异常 0代表不推荐 数字越大代表推荐程度越高 范围为1-5
    def levelOfSale(self,date,index):
        pass

    def levelOfVolume(self,date,index):
        if index<5:
                return 0

        else:
            dataList = []
            for i in range(0,6):
                dataList.append({'daydata':self.dayData.get(date = self.getDateBefore(date,i))})

            if (dataList[1]['daydata'].volume+dataList[2]['daydata'].volume+dataList[3]['daydata'].volume+dataList[4]['daydata'].volume+dataList[5]['daydata'].volume)/5*4>dataList[0]['daydata'].volume:
                return 0.4
            if (dataList[1]['daydata'].volume+dataList[2]['daydata'].volume+dataList[3]['daydata'].volume+dataList[4]['daydata'].volume+dataList[5]['daydata'].volume)/5*3>dataList[0]['daydata'].volume:
                return 0.3
            if (dataList[1]['daydata'].volume+dataList[2]['daydata'].volume+dataList[3]['daydata'].volume+dataList[4]['daydata'].volume+dataList[5]['daydata'].volume)/5*2>dataList[0]['daydata'].volume:
                return 0.2
            if (dataList[1]['daydata'].volume+dataList[2]['daydata'].volume+dataList[3]['daydata'].volume+dataList[4]['daydata'].volume+dataList[5]['daydata'].volume)/5*1>dataList[0]['daydata'].volume:
                return 0.1

        return 0
    def isNormalVolume(self,date,index):
        if index<5:
            return 0
        else:
            dataList = []
            for i in range(0,6):
                dataList.append({'daydata':self.dayData.get(date = self.getDateBefore(date,i))})
            if (dataList[1]['daydata'].volume+dataList[2]['daydata'].volume+dataList[3]['daydata'].volume+dataList[4]['daydata'].volume+dataList[5]['daydata'].volume)/5*1.2>dataList[0]['daydata'].volume and \
                            dataList[0]['daydata'].volume>0.8*(dataList[1]['daydata'].volume+dataList[2]['daydata'].volume+dataList[3]['daydata'].volume+dataList[4]['daydata'].volume+dataList[5]['daydata'].volume)/5:
                return 1
        return 0
    def isHighVolume(self,date,index):
        if index<5:
            return 0
        else:
            dataList = []
            for i in range(0,6):
                dataList.append({'daydata':self.dayData.get(date = self.getDateBefore(date,i))})
            if (dataList[1]['daydata'].volume+dataList[2]['daydata'].volume+dataList[3]['daydata'].volume+dataList[4]['daydata'].volume+dataList[5]['daydata'].volume)/5*2<dataList[0]['daydata'].volume:
                return 1
        return 0
#判断上影线是否短
    def isShortUS(self,date):
        data = self.dayData.get(date = date)

        if data.close>data.open:
            if (data.high-data.close)/data.close<=0.01:
                return 1
        if data.open>data.close:
            if (data.high-data.open)/data.open<=0.01:
                return 1
        return 0
#判断下影线是否短
    def isShortLS(self,date):
        data = self.dayData.get(date = date)
        if data.close>data.open:
            if (data.open-data.low)/data.open<=0.01:
                return 1
        if data.open>data.close:
            if (data.close-data.low)/data.close<=0.01:
                return 1
        return 0

#   判断当前股价是否处在上升阶段
    def isRising(self,date,index):
        data = self.maData.get(date = date)
        min=(float)(self.getLowPoint(date,index))
        if min!=0 and self.isUpMa20(date,index):
#    4   10  0.12
            if (data.ma5-min)/min>0.12:
                return 1
        if min!=0 and self.isUpMa20(date,index)==0:
#    4   10  0.10
            if (data.ma5-min)/min>0.10:
                return 1
        return 0
#   判断当前股价是否处在下降阶段 new
    def isDescending(self,date,index):
        data = self.maData.get(date = date)
        max=(float)(self.getHighPoint(date,index))
        if max!=0 and self.isUpMa20(date,index):
#    10  0.10
            if (max-data.ma5)/max>0.15:
                return 1
#    10  0.20
        if max!=0 and self.isUpMa20(date,index)==0:
            if (max-data.ma5)/max>0.30:
                return 1
        return 0
#    判断当前是否横
    def isTransverse(self,date):
        return 1
#    判断是否在二十日均线上
    def isUpMa20(self,date,index):
        dataList = []
        for i in range(0,2):
            dataList.append({'daydata':self.dayData.get(date = self.getDateBefore(date,i)),
                             'madata':self.maData.get(date = self.getDateBefore(date,i))})

        if index>3 and dataList[0]['madata'].ma20<(dataList[0]['daydata'].close+dataList[1]['daydata'].close)/2:
            return 1
        else:
            return 0
#        获取前一段时间的股价高点
    def getHighPoint(self,date,index):
        max=0.0
        if index>=9:
            max = self.maData.filter(date__lte = date).order_by('-ma5')[0].ma5
        return max

#    获取前一段时间的股价低点
    def getLowPoint(self,date,index):
        min=100000.0
        if index>=9:
            min = self.maData.filter(date__lte = date).order_by('ma5')[0].ma5
        return min
#   判断收盘价在前一天中点以上
    def isUpperMiddle(self,date):
        dataList = []
        for i in range(0,2):
            dataList.append({'daydata':self.dayData.get(date = self.getDateBefore(date,i)),
                             'madata':self.maData.get(date = self.getDateBefore(date,i))})

        if dataList[0]['daydata'].close>(dataList[1]['daydata'].open+dataList[1]['daydata'].close)/2:
            return 1
        return 0
#    判断当天k线与前一天是否有缺口
    def hasBreach(self,date):
        yesterday = self.getDateBefore(date,1)
        dataList = []
        for i in range(0,2):
            dataList.append({'daydata':self.dayData.get(date = self.getDateBefore(date,i))})

        breach=0.01
        if self.isUpper(yesterday):
            if self.isUpper(date) and (dataList[0]['daydata'].open-dataList[1]['daydata'].close)/dataList[1]['daydata'].close>breach:
                return 1
            if self.isLower(date) and (dataList[0]['daydata'].close-dataList[1]['daydata'].close)/dataList[1]['daydata'].close>breach:
                return 1
        if self.isLower(yesterday):
            if self.isUpper(date) and (dataList[1]['daydata'].close-dataList[0]['daydata'].close)/dataList[1]['daydata'].close>breach:
                return 1
            if self.isLower(date) and (dataList[1]['daydata'].close-dataList[0]['daydata'].open)/dataList[1]['daydata'].close>breach:
                return 1
        return 0
#    判断收盘价在前一天中点以下
    def isLowerMiddle(self,date):
        dataList = []
        for i in range(0,2):
            dataList.append({'daydata':self.dayData.get(date = self.getDateBefore(date,i))})

        if dataList[0]['daydata'].close<(dataList[1]['daydata'].open+dataList[1]['daydata'].close)/2:
            return 1
        return 0
#     判断当天是否为阳线
    def isUpper(self,date):
        data = self.dayData.get(date = date)
        if data.close>data.open:
            return 1
        return 0
#    判断当前是否为阴线
    def isLower(self,date):
        data= self.dayData.get(date = date)
        if data.close<data.open:
            return 1
        return 0
    '''
    def getIndexOfDate(self,date):
        length=len(self.result)
        for i in range(0,length):
            if (date-self.result[i][0]).total_seconds()==0:
                return i
        return -1
    '''
#   获取当天股票的涨跌幅绝对值ֵ
    def rate(self,date):
        data = self.dayData.get(date = date)
        return abs((data.close-data.open)/data.open)

    def getDateBefore(self,date,dif):
        dayData = self.dayData.filter(date__lte = date).order_by('-date')[dif]
        resultDate = dayData.date
        return resultDate
