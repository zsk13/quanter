from quanter.strategy import *
import pandas as pd

class Trade(object):
    def __init__(self, bars, strategy = MAStrategy(), init_capital = 100000.0):
        self.bars = bars
        self.init_capital = init_capital
        self.strategy = strategy

    def setStrategy(self, strategy):
        self.strategy = strategy

    def trade_tracing(self):
        if len(self.bars)==0:
            capital = pd.DataFrame()
            capital['yieldRate'] = 0
            return capital
        flag = self.strategy.gen_signal(self.bars)
        amounts = pd.Series(index = flag.index)
        total = pd.Series(index = flag.index)
        index = flag.index
        price = self.bars['close']
        
        tempTotal = self.init_capital

        holdNum = 0
        for i,x in enumerate(flag):
            if x==1:
                if holdNum == 0:
                    holdNum = tempTotal/price[index[i]]
                else:
                    tempTotal = holdNum * price[index[i]]
            elif x ==-1:
                if holdNum != 0:
                    tempTotal = holdNum * price[index[i]]
                    holdNum = 0
                else:
                    pass
            amounts[i] = holdNum
            total[i] = tempTotal

        capital = pd.DataFrame(index = flag.index)
        capital['total'] = total
        capital['yieldRate'] = (capital['total'] - self.init_capital)/self.init_capital
        return capital

    def getSuccessRate(self):
        if len(self.bars)==0:
            return 0
        flag = self.strategy.gen_signal(self.bars)
        y = self.bars['close'].diff()>0
        y = y*2-1
        rate = float(sum(flag[:-1]==y[1:]))/(len(flag)-1)
        return rate