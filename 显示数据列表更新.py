import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'gupiao.settings'
import django
django.setup()
from login import models
import pandas as pd

a=models.Allshujuname.objects.all()
zd={}
for i in a:
    zd[i.name]=i.filters
print(zd)
