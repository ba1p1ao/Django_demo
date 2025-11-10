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
