from django.db import models
from django.conf import settings
# Create your models here.
# class User(models.Model):
#     name = models.CharField(max_length=128,unique=True)
#     password = models.CharField(max_length=256)
#     mobile = models.CharField(max_length=50,unique=True)
#     sex = models.CharField(max_length=32,choices=(('male','男'),('female','女')),default='男')
#     c_time = models.DateTimeField(auto_now_add=True)
#     def __str__(self):
#         return self.name
#     class Meta:
#         ordering = ['c_time']
#
