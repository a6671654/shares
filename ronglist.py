import pandas as pd
import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'gupiao.settings'
import django
django.setup()
from main import models

a=pd.read_csv('rong.csv',index_col=0)

for i in a.index:
    code=a.loc[i,'ts_code']
    code=code[-2:].lower()+'.'+code[:-3]
    try:
        codeojb=models.Gupiaolist.objects.get(code=code)
        codeojb.liangrong=True
        codeojb.save()
    except:
        print(code)

