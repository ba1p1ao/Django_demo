from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.http import require_http_methods

# Create your views here.


@require_http_methods(["POST"])  # 注意，中括号中的请求方法名务必大写!!!否则无法正常显示
def index(request):
    data = "<h1>hello user/index</h1>"
    return HttpResponse(data, content_type="text/html")


@require_http_methods(["GET"])
def users(request):
    data = "<h1>hello user/users</h1>"
    return HttpResponse(data, content_type="text/html")

# 如果不写 require_http_methods，默认可以接受所有类型的请求
def getAllarges(request):
    
    ## http://localhost:8001/users/info/?username=admin&password=123
    print(request.GET) # <QueryDict: {'username': ['admin'], 'password': ['123']}>
    print(request.GET.get("username")) # admin
    print(request.GET.get("password")) # 123
    print(request.GET["password"]) # 123


    ## 如果有多个相同的参数请求
    ## http://localhost:8001/users/info/?username=admin&password=123&love=youxi&love=xuexi&love=yundong
    print(request.GET)  # <QueryDict: {'username': ['admin'], 'password': ['123'], 'love': ['youxi', 'xuexi', 'yundong']}>
    print(request.GET.get("username")) # admin
    print(request.GET.get("password")) # 123
    print(request.GET.get("love")) # 会覆盖love的值 # yundong
    print(request.GET.getlist("love")) # 不会覆盖love的值，会返回列表的形式 # ['youxi', 'xuexi', 'yundong']
    
    ## POST 请求 直接调用 POST，
    print(request.POST) # 显示的请求体内容


    return HttpResponse("ok")