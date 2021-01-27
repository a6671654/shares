from django.contrib import admin

# Register your models here.
from .models import Gupiaolist,Jiaoyiday

class gupiaoliebiao(admin.ModelAdmin):
    list_display = ['code','codename']
    search_fields = ['code','codename']

class Lei(admin.ModelAdmin):
    actions_on_bottom = True
    list_display = ['date','isover']
    ordering = ['date']
    readonly_fields = ['isover']
    search_fields = ['text']

admin.site.register(Gupiaolist,gupiaoliebiao)
admin.site.register(Jiaoyiday,Lei)