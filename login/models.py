from django.db import models
from django.conf import settings
# Create your models here.
class Alluser(models.Model):
    name = models.CharField(max_length=128,unique=True)
    password = models.CharField(max_length=256)
    mobile = models.CharField(max_length=50,unique=True)
    sex = models.CharField(max_length=32,choices=(('male','男'),('female','女')),default='男')
    c_time = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.name
    class Meta:
        ordering = ['c_time']

class Celve(models.Model):
    clcode = models.CharField(max_length=256,unique=True)
    clname = models.TextField(max_length=256)
    last_time = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return  self.clname

class usercelve(models.Model):
    user = models.ForeignKey(Alluser,on_delete=models.CASCADE)
    celve = models.ForeignKey(Celve,on_delete=models.CASCADE)
    clname = models.CharField(max_length=256)
    nums = models.IntegerField(default=0)
    last_time = models.DateTimeField(auto_now_add=True)
    shanchu = models.FloatField(null=True)
    def __str__(self):
        return self.user.name + ':' + self.clname