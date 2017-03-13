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

    def __unicode__(self):
        return self.name

class DayData(models.Model):
    date = models.DateField()
    open_price = models.FloatField()
    high = models.FloatField()
    low = models.FloatField()
    close = models.FloatField()
    trade_status = models.CharField(max_length=50)
    volume = models.IntegerField()
    amt = models.IntegerField()
    stock = models.ForeignKey(Stock)

    def __unicode__(self):
        return self.trade_status