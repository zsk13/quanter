from django.db import models

# Create your models here.
class Mysite(models.Model):
    title = models.CharField(max_length=100)
    url = models.URLField()
    author = models.CharField(max_length=100)
    num = models.IntegerField(max_length=10)

    def __unicode__(self):
        return self.title


class Stock(models.Model):
    code = models.CharField(max_length=50,primary_key=True)
    name = models.CharField(max_length=50)
    isInPool = models.BooleanField(default=1)

    def __unicode__(self):
        return self.name

class DayData(models.Model):
    date = models.DateField()
    open = models.FloatField()
    high = models.FloatField()
    low = models.FloatField()
    close = models.FloatField()
    status = models.CharField(max_length=50)
    volume = models.FloatField()
    amt = models.FloatField()
    stock = models.ForeignKey(Stock)

    def __unicode__(self):
        return self.trade_status

class MAData(models.Model):
    date = models.DateField()
    stock = models.ForeignKey(Stock)
    ma5 = models.FloatField()
    ma10 = models.FloatField()
    ma20 = models.FloatField()
    ma60 = models.FloatField()
    ma120 = models.FloatField()

    def __unicode__(self):
        return self.ma5

class KDJData(models.Model):
    date = models.DateField()
    stock = models.ForeignKey(Stock)
    RSV = models.FloatField()
    K = models.FloatField()
    D = models.FloatField()
    J = models.FloatField()

class ProfitRateData(models.Model):
    year = models.IntegerField()
    stock = models.ForeignKey(Stock)
    strategy = models.CharField(max_length=50)
    profitRate = models.FloatField()

class Foundamental(models.Model):
    code = models.CharField(max_length=50)
    name = models.CharField(max_length=50)
    year = models.IntegerField()
    quarter = models.IntegerField()
    eps = models.FloatField()
    bvps = models.FloatField()
    roe = models.FloatField()
    epcf = models.FloatField()
    net_profits = models.FloatField()
    report_date = models.DateField()
    net_profit_ratio = models.FloatField()
    gross_profit_rate= models.FloatField()
    business_income= models.FloatField()
    bips= models.FloatField()
    arturnover= models.FloatField()
    arturndays= models.FloatField()
    inventory_turnover= models.FloatField()
    inventory_days= models.FloatField()
    currentasset_turnover= models.FloatField()
    currentasset_days= models.FloatField()
    mbrg= models.FloatField()
    nprg= models.FloatField()
    nav= models.FloatField()
    targ= models.FloatField()
    epsg= models.FloatField()
    seg= models.FloatField()
    currentratio= models.FloatField()
    quickratio= models.FloatField()
    cashratio= models.FloatField()
    icratio= models.FloatField()
    sheqratio= models.FloatField()
    adratio= models.FloatField()
    cf_sales= models.FloatField()
    rateofreturn= models.FloatField()
    cf_nm= models.FloatField()
    cf_liabilities= models.FloatField()
    cashflowratio = models.FloatField()
    signal = models.IntegerField()

    def __unicode__(self):
        return self.code

    def to_array(self):
        result = []
        result.append(self.eps )
        result.append(self.bvps )
        result.append(self.roe )
        result.append(self.epcf )
        result.append(self.net_profits )
        result.append(self.net_profit_ratio )
        result.append(self.gross_profit_rate)
        result.append(self.business_income)
        result.append(self.bips)
        result.append(self.arturnover)
        result.append(self.arturndays)
        result.append(self.inventory_turnover)
        result.append(self.inventory_days)
        result.append(self.currentasset_turnover)
        result.append(self.currentasset_days)
        result.append(self.mbrg)
        result.append(self.nprg)
        result.append(self.nav)
        result.append(self.targ)
        result.append(self.epsg)
        result.append(self.seg)
        result.append(self.currentratio)
        result.append(self.quickratio)
        result.append(self.cashratio)
        result.append(self.icratio)
        result.append(self.sheqratio)
        result.append(self.adratio)
        result.append(self.cf_sales)
        result.append(self.rateofreturn)
        result.append(self.cf_nm)
        result.append(self.cf_liabilities)
        result.append(self.cashflowratio )
        return result