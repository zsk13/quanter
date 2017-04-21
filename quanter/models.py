# encoding: UTF-8
from django.db import models
from users.models import *


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
        return str(self.date)

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

class StockPool(models.Model):
    userId = models.ForeignKey(User)
    stockCode =  models.CharField(max_length=50)

class StockGroup(models.Model):
    id = models.AutoField(primary_key=True)
    userId = models.ForeignKey(User)
    groupName = models.CharField(max_length=200)

class GroupContent(models.Model):
    id = models.AutoField(primary_key=True)
    groupId = models.ForeignKey(StockGroup)
    stockCode =  models.CharField(max_length=50)

class stock_basic(models.Model):
    code = models.CharField(max_length=50, primary_key=True)
    name = models.CharField(max_length=100)
    industry = models.CharField(max_length=100)
    area = models.CharField(max_length=100)
    pe = models.FloatField()
    outstanding = models.FloatField()
    totals = models.FloatField()
    totalAssets = models.FloatField()
    liquidAssets = models.FloatField()
    fixedAssets = models.FloatField()
    reserved = models.FloatField()
    reservedPerShare = models.FloatField()
    esp = models.FloatField()
    bvps = models.FloatField()
    pb = models.FloatField()
    timeToMarket = models.BigIntegerField()
    undp = models.FloatField()
    perundp = models.FloatField()
    rev = models.FloatField()
    profit = models.FloatField()
    gpr = models.FloatField()
    npr = models.FloatField()
    holders = models.BigIntegerField()

class dailydata(models.Model):
    code = models.CharField(max_length=50)
    date = models.DateField()
    open = models.FloatField()
    high = models.FloatField()
    low = models.FloatField()
    close = models.FloatField()
    volume = models.FloatField()
    price_change = models.FloatField()
    p_change = models.FloatField()
    ma5 = models.FloatField()
    ma10 = models.FloatField()
    v_ma5 = models.FloatField()
    v_ma10 = models.FloatField()
    v_ma20 = models.FloatField()
    turnover = models.FloatField()


    def to_array(self):
        result = []
        result.append(self.open)
        result.append(self.high)
        result.append(self.low)
        result.append(self.close)
        result.append(self.volume)
        result.append(self.price_change )
        result.append(self.p_change)
        result.append(self.ma5)
        result.append(self.ma10)
        result.append(self.v_ma5)
        result.append(self.v_ma10)
        result.append(self.v_ma20)
        result.append(self.turnover)
        result.append(self.lastopen)
        result.append(self.lasthigh)
        result.append(self.lastlow)
        result.append(self.lastclose)
        result.append(self.lastvolume)
        return result

    def to_array_for_hs_300(self):
        result = []
        result.append(self.open)
        result.append(self.high)
        result.append(self.low)
        result.append(self.close)
        result.append(self.volume)
        result.append(self.lastopen)
        result.append(self.lasthigh)
        result.append(self.lastlow)
        result.append(self.lastclose)
        result.append(self.lastvolume)
        return result