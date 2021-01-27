from django.db import models
from django.conf import settings
from ckeditor.fields import RichTextField
# Create your models here.
class Alluser(models.Model):
    name = models.CharField(max_length=128,unique=True)
    password = models.CharField(max_length=256)
    mobile = models.CharField(max_length=50,null=True)
    sex = models.CharField(max_length=32,choices=(('male','男'),('female','女')),default='male')
    c_time = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.name
    class Meta:
        ordering = ['c_time']

class Celve(models.Model):
    clcode = models.CharField(max_length=255,unique=True)
    clname = models.TextField(max_length=256)
    last_time = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return  self.clname

class Ziliao(models.Model):
    user = models.OneToOneField(Alluser,on_delete=models.CASCADE)
    xianshi = models.CharField(max_length=256,null=True)

class usercelve(models.Model):
    user = models.ForeignKey(Alluser,on_delete=models.CASCADE)
    celve = models.ForeignKey(Celve,on_delete=models.CASCADE)
    clname = models.CharField(max_length=256)
    nums = models.IntegerField(default=0)
    last_time = models.DateTimeField(auto_now_add=True)
    shanchu = models.NullBooleanField(null=True)
    xianshi = models.CharField(max_length=256,null=True)
    def __str__(self):
        return self.user.name + ':' + self.clname

class Allshujuname(models.Model):
    name = models.CharField(max_length=256)
    jieshi = models.CharField(max_length=256)
    filters = models.CharField(max_length=256)
    def __str__(self):
        return self.name

class Update(models.Model):
    biaoti= models.CharField(max_length=255)
    neirong = RichTextField()
    updateday = models.DateField()
    def __str__(self):
        return self.biaoti