from django.db import models

# Create your models here.

class Gupiaolist(models.Model):
    code = models.CharField(max_length=9,verbose_name='股票代码')
    codename = models.CharField(max_length=20,verbose_name='股票名称')
    def __str__(self):
        return str(self.code)

class Jiaoyiday(models.Model):
    date = models.DateField(auto_now=False, auto_now_add=False)
    isover = models.NullBooleanField(null=True)
    def __str__(self):
        return str(self.date)
class kline(models.Model):
    code = models.ForeignKey(Gupiaolist,on_delete=models.CASCADE)
    date = models.ForeignKey(Jiaoyiday,on_delete=models.CASCADE)
    open = models.FloatField(null=True)
    close = models.FloatField(null=True)
    high = models.FloatField(null=True)
    low = models.FloatField(null=True)
    volume = models.FloatField(null=True)
    preclose = models.FloatField(null=True)
    turn = models.FloatField(null=True)
    dif = models.FloatField(null=True)
    dea = models.FloatField(null=True)
    hist = models.FloatField(null=True)
    kdjK = models.FloatField(null=True)
    kdjD = models.FloatField(null=True)
    kdjJ = models.FloatField(null=True)
    day5 = models.FloatField(null=True)
    day10 = models.FloatField(null=True)
    day20 = models.FloatField(null=True)
    upper = models.FloatField(null=True)
    middle = models.FloatField(null=True)
    lower = models.FloatField(null=True)
    def __str__(self):
        return str(self.code.code)+str(self.code.codename)
class jisuan(models.Model):
    code = models.ForeignKey(Gupiaolist,on_delete=models.CASCADE)
    date = models.ForeignKey(Jiaoyiday,on_delete=models.CASCADE)
    day5to10 = models.NullBooleanField(null=True)
    day5to20 = models.NullBooleanField(null=True)
    day10to20 = models.NullBooleanField(null=True)
    MACD = models.NullBooleanField(null=True)
    buynumtwo = models.NullBooleanField(null=True)
    buynum5 = models.NullBooleanField(null=True)
    buynum20 = models.NullBooleanField(null=True)
    KDJ = models.NullBooleanField(null=True)
    buynum3up = models.NullBooleanField(null=True)
    buynum5up = models.NullBooleanField(null=True)
    buynum3chang = models.NullBooleanField(null=True)
    buynum5chang = models.NullBooleanField(null=True)
    day5keep5 = models.NullBooleanField(null=True)
    day5keep10 = models.NullBooleanField(null=True)
    day5keep20 = models.NullBooleanField(null=True)
    MACD3up = models.NullBooleanField(null=True)
    MACD5up = models.NullBooleanField(null=True)
    MACD3chang = models.NullBooleanField(null=True)
    MACD3chang2 = models.NullBooleanField(null=True)
    MACD5chang = models.NullBooleanField(null=True)
    MACD5chang2 = models.NullBooleanField(null=True)
    BOLL3big = models.NullBooleanField(null=True)
    BOLL5big = models.NullBooleanField(null=True)

    def __str__(self):
        return str(self.code.code)+str(self.code.codename)