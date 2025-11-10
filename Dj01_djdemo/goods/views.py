from django.shortcuts import render
from django.http.response import HttpResponse
from django.views.decorators.http import require_http_methods
# Create your views here.

# 让用户发送POST才能访问的页面
# 用于限制用户访问函数视图的http访间方法
@require_http_methods(["POST"]) # 注意，中括号中的请求方法名务必大写!!!否则无法正常显示
def index(request):
    data = "<h1>hello goods/index</h1>"
    return HttpResponse(data, content_type="text/html")



@require_http_methods(["GET"]) 
def goods(request):
    data = "<h1>hello goods/goods</h1>"
    return HttpResponse(data, content_type="text/html")