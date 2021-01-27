from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import HttpResponse

heilist=['127.0.0.1']
#创建自己的中间件
class Mymidd(MiddlewareMixin):
    #定义请求入口
    def process_request(self,request):
        print('一个请求进来了')
    #被处理完毕后的请求经过,必须要return response
    def process_response(self,request,response):
        print('请求被处理完毕')
        return response