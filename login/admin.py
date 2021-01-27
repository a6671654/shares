from django.contrib import admin

# Register your models here.
from .models import Alluser,usercelve,Allshujuname,Update


class Updateclass(admin.ModelAdmin):
    list_display = ['biaoti', 'updateday']

class alluserclass(admin.ModelAdmin):
    list_display = ['name','c_time','last_login']

class celce(admin.ModelAdmin):
    list_display = ['user', 'celve', 'clname','nums','last_time','shanchu']


admin.site.register(Alluser,alluserclass)
admin.site.register(usercelve,celce)
admin.site.register(Allshujuname)
admin.site.register(Update,Updateclass)