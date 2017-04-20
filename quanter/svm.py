import tushare as ts
import pandas as pd
import numpy as np
from sklearn import svm  
from sqlalchemy import create_engine
from models import *
from  datetime  import  *  
from sklearn.model_selection import GridSearchCV
from sklearn.decomposition import PCA
from sklearn import preprocessing 

# class SVMStrategy(object):
#     def __init__(self):
#         pass

#     def svmTraining(self, x, y):
#         self.clf = svm.SVC() 
#         self.clf.fit(x, y)

#     def svmPredict(self, x):
#         y = self.clf.predict(x)
#         return y

class Data(object):
    def __init__(self, year, quarter):
        self.year = year
        self.quarter = quarter

    def get_report_data_from_db(self):
        stock_info=ts.get_today_all()
        foundamentalDatas = Foundamental.objects.filter(year=self.year,quarter=self.quarter)
        x=[]
        y=[]
        code = []
        name = []
        for data in foundamentalDatas:
            if data.code not in code :
                temp = stock_info[stock_info['code'].isin([data.code])]
                if not temp.empty:
                    name.append(temp.iloc[0,1])
                    x.append(data.to_array())
                    code.append(data.code)
                    y.append(data.signal)

        return code,x,y,name

    def get_report_data(self):
        end_date=str(self.year+1) + '-01-01'
        end_date2=str(self.year+1) + '-01-10'


        report = ts.get_report_data(self.year, self.quarter)
        report.drop_duplicates(['code'])
        report = report.set_index('code')
        report.drop(['eps_yoy','profits_yoy','distrib'],axis=1, inplace=True)
        report = report.replace('NaN',0)


        profit = ts.get_profit_data(self.year, self.quarter)
        profit.drop(['name','net_profits','eps','roe'],axis=1, inplace=True)
        profit.drop_duplicates(['code'])
        profit = profit.set_index('code')
        profit = profit.replace('NaN',0)


        operation = ts.get_operation_data(self.year, self.quarter)
        operation.drop_duplicates(['code'])
        operation = operation.set_index('code')
        operation.drop(['name'],axis=1, inplace=True)
        operation = operation.replace('NaN',0)
        

        growth = ts.get_growth_data(self.year, self.quarter)
        growth.drop_duplicates(['code'])
        growth = growth.set_index('code')
        growth.drop(['name'],axis=1, inplace=True)
        growth = growth.replace('NaN',0)
        

        debtpaying = ts.get_debtpaying_data(self.year, self.quarter)
        debtpaying.drop_duplicates(['code'])
        debtpaying = debtpaying.set_index('code')
        debtpaying.drop(['name'],axis=1, inplace=True)
        debtpaying = debtpaying.replace('NaN',0)
        

        cashflow = ts.get_cashflow_data(self.year, self.quarter)
        cashflow.drop_duplicates(['code'])
        cashflow = cashflow.set_index('code')
        cashflow.drop(['name'],axis=1, inplace=True)
        cashflow = cashflow.replace('NaN',0)
        

        # 
        # 
        # debtpaying = ts.get_debtpaying_data(self.year, self.quarter)
        # cashflow = ts.get_cashflow_data(self.year, self.quarter)
        result = report.join(profit).join(operation).join(growth).join(debtpaying).join(cashflow)
        result = result.replace('NaN',0)
        result = result.replace(np.NaN,0)
        result = result.replace("--", 0)
        result['year'] = self.year
        result['quarter'] = self.quarter
        result = result.fillna(0)
        code=[]
        dates=[]
        for index, row in result.iterrows():
            if index not in code:
                code.append(index)
                dates.append(row['report_date'])
                f = Foundamental()
                f.year=self.year
                f.quarter=self.quarter
                f.code=index
                # f.name=row['name'].decode('gb2312').encode('utf-8')
                report_date = row['report_date'].split('-')
                f.report_date = date(year=self.year,month=int(report_date[0]),day=int(report_date[1]))
                f.eps = row['eps']
                f.bvps = row['bvps']
                f.roe = row['roe']
                f.epcf = row['epcf']
                f.net_profits = row['net_profits']
                f.net_profit_ratio = row['net_profit_ratio']
                f.gross_profit_rate= row['gross_profit_rate']
                f.business_income= row['business_income']
                f.bips= row['bips']
                f.arturnover= row['arturnover']
                f.arturndays= row['arturndays']
                f.inventory_turnover= row['inventory_turnover']
                f.inventory_days= row['inventory_days']
                f.currentasset_turnover= row['currentasset_turnover']
                f.currentasset_days= row['currentasset_days']
                f.mbrg= row['mbrg']
                f.nprg= row['nprg']
                f.nav= row['nav']
                f.targ= row['targ']
                f.epsg= row['epsg']
                f.seg= row['seg']
                f.currentratio= row['currentratio']
                f.quickratio= row['quickratio']
                f.cashratio= row['cashratio']
                f.icratio= row['icratio']
                f.sheqratio= row['sheqratio']
                f.adratio= row['adratio']
                f.cf_sales= row['cf_sales']
                f.rateofreturn= row['rateofreturn']
                f.cf_nm= row['cf_nm']
                f.cf_liabilities= row['cf_liabilities']
                f.cashflowratio = row['cashflowratio']
                end_price = ts.get_hist_data(code=f.code,start=end_date,end=end_date2)
                if end_price.empty:
                    end_close=0
                else:
                    end_close = end_price.iloc[0,2]
                start_date = f.report_date.strftime('%Y-%m-%d')
                start_price = ts.get_hist_data(code=f.code,start=start_date,end=start_date)
                if start_price.empty:
                    start_close=0
                else:
                    start_close = start_price.iloc[0,2]
                if start_close!=0 and end_close/start_close>1.1:
                    f.signal=1
                else:
                    f.signal=0
                f.save()
        return result


class GridSearch(object):
    def getClassifier(self, x, y):
        parmeters = {'C':[1,2,4,8,16,32], 'gamma':[0.125, 0.25, 0.5 ,1, 2, 4, 8]}
        svc = svm.SVC()
        clf = GridSearchCV(svc, parmeters, n_jobs=-1, cv=3)
        clf.fit(x,y)
        return clf

    def defaultData(self, code="600317"):
        s = StockData()
        if code=='399300':
            data = s.get_hs300_data()
        else:
            data = s.getData(code)

        scaler = preprocessing.StandardScaler().fit(data[0])
        normaldata = scaler.transform(data[0])

        pca=PCA(n_components=5)
        newData=pca.fit_transform(normaldata)
        return newData,data[1],data[2]

