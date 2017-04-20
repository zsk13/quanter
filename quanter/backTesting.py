import pandas
import numpy as np

class MAStrategy(object):
    def __init__(self,bars,short_window=5, long_window=20):
        self.bars = bars
        self.short_window = short_window
        self.long_window = long_window

    def MA(self, price, windows = 5, period = 1):
        MAprice = pandas.rolling_mean(price, windows, period)
        return MAprice

    def gen_signal(self):
        signals = pandas.DataFrame(index = self.bars.index)
        signals['flag'] = 0
        signals['sma'] = self.MA(self.bars['close'],self.short_window,1)
        signals['lma'] = self.MA(self.bars['close'],self.long_window,1)
        signals.loc[self.short_window:,['flag']] = np.where(signals['sma'][self.short_window:]>signals['lma'][self.short_window:],1,0)
        signals['signal'] = signals['flag'].diff().fillna(signals['flag'][0])

        return signals

class MATrade(object):
    def __init__(self, bars, signals, init_capital = 100000.0):
        self.bars = bars
        self.init_capital = init_capital
        self.signals = signals

    def gen_position(self):
        positions = self.signals['flag']*1000
        return positions

    def trade_positions(self):
        positions = self.signals['signal']*1000
        return positions

    def trade_tracing(self):
        capital = pandas.DataFrame(index = self.signals.index)
        capital['hold'] = self.gen_position()*self.bars['close']
        capital['rest'] = self.init_capital - (self.trade_positions()*self.bars['close']).cumsum()
        capital['total'] = capital['hold']+capital['rest']
        capital['return'] = capital['total'].pct_change().fillna(capital['total'][0]/self.init_capital-1)
        capital['yieldRate'] = (capital['total'] - self.init_capital)/self.init_capital
        return capital

# if __name__ == '__main__':
#     bars = tushare.get_h_data('603901',start='2012-01-01', end='2016-01-01').sort_index()
#     test_strategy = MAStrategy(bars)
#     signals = test_strategy.gen_signal()
#     test_trade = MATrade(bars,signals)
#     captial = test_trade.trade_tracing()        
#     print captial