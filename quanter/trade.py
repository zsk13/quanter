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
        signal = flag.diff().fillna(flag[0])
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

        # tradeAmounts = amounts.diff().fillna(amounts[0])

        capital = pd.DataFrame(index = flag.index)
        # capital['hold'] = amounts*self.bars['close']
        # capital['rest'] = self.init_capital - (self.trade_positions()*self.bars['close']).cumsum()
        capital['total'] = total
        # capital['return'] = capital['total'].pct_change().fillna(capital['total'][0]/self.init_capital-1)
        capital['yieldRate'] = (capital['total'] - self.init_capital)/self.init_capital
        return capital