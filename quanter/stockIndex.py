import pandas as pd

class StockIndex(object):
    def __init__(self, close = None, open = None, high = None, low = None, volume=None):
        self.close = close
        self.open = open
        self.high = high
        self.low = low
        self.volume = volume

    def MA(self, price = None, windows = 5, period = 1):
        if price is None:
            price = self.close
        MAprice = pd.rolling_mean(price, windows, period)
        return MAprice

    def BIAS(self, price = None, n = 6):
        if price is None:
            price = self.close
        ma = self.MA(price = price, windows = n)
        bias = 100 * (price - ma)/ma
        return bias

    def PSY(self, price = None, n = 12):
        if price is None:
           price = self.close
        diff = price.diff().fillna(1)
        up = diff>0
        psy = pd.rolling_apply(up,window = n, func = lambda x: 100*sum(x)/len(x),min_periods = 1)
        return psy

    def RSV_K_D_J(self, N=9, N2 = 3, N3 = 3):
        minlow = pd.rolling_min(self.low,window = N, min_periods=1)
        maxhigh = pd.rolling_max(self.high, window=N,min_periods=1)
        RSV = (self.close-minlow)/(maxhigh-minlow)*100
        K = self.MA(RSV,windows = N2)
        D = self.MA(K,windows = N3)
        J = D*3-K*2
        return RSV,K,D,J

    def RSI(self, N = 6):
        diff = self.close.diff().fillna(1)
        up = diff > 0
        down = diff < 0
        updiff = up * diff
        downdiff = down * diff
        uptotal = pd.rolling_sum(updiff,window = N, min_periods=1)
        downtotal = -pd.rolling_sum(downdiff,window = N, min_periods=1)
        rsi = 100 * uptotal/(uptotal+downtotal)
        return rsi

    def WR(self, N = 14):
        minlow = pd.rolling_min(self.low,window = N, min_periods=1)
        maxhigh = pd.rolling_max(self.high, window=N,min_periods=1)
        wr = 100 * (maxhigh - self.close)/(maxhigh - minlow)
        return wr

    def getNeedData(self):
        bias6 = self.BIAS(n=6)
        # bias12 = self.BIAS(n=12)
        # bias24 = self.BIAS(n=24)
        psy12 = self.PSY(n=12)
        # psy24 = self.PSY(n=24)
        RSV,K,D,J = self.RSV_K_D_J()
        rsi6 = self.RSI(N=6)
        # rsi12 = self.RSI(N=12) 
        # rsi24 = self.RSI(N=24)
        wr = self.WR(N=14)
        df = pd.DataFrame()
        df['bias6'] = bias6
        # df['bias12'] = bias12
        # df['bias24'] = bias24
        df['psy12'] = psy12 
        # df['psy24'] = psy24 
        df['RSV'] = RSV
        df['K'] = K
        df['D'] = D
        df['J'] = J
        df['rsi6'] = rsi6
        # df['rsi12'] = rsi12
        # df['rsi24'] = rsi24
        df['wr'] = wr
        # return bias6,bias12,bias24,psy12,psy24,RSV,K,D,J,rsi6,rsi12,rsi24,wr
        return df