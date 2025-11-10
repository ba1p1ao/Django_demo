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
def getAllargs(request):

    ## http://localhost:8001/users/info/?username=admin&password=123
    print(request.GET)  # <QueryDict: {'username': ['admin'], 'password': ['123']}>
    print(request.GET.get("username"))  # admin
    print(request.GET.get("password"))  # 123
    print(request.GET["password"])  # 123
    print(request.GET.get("size", "0"))  # 如果没有size 参数，返回 0 字符串
    print(request.GET.getlist("size", ["0"]))  # 如果没有size 参数，返回 ["0"]

    ## 如果有多个相同的参数请求
    ## http://localhost:8001/users/info/?username=admin&password=123&love=youxi&love=xuexi&love=yundong
    print(
        request.GET
    )  # <QueryDict: {'username': ['admin'], 'password': ['123'], 'love': ['youxi', 'xuexi', 'yundong']}>
    print(request.GET.get("username"))  # admin
    print(request.GET.get("password"))  # 123
    print(request.GET.get("love"))  # 会覆盖love的值 # yundong
    print(
        request.GET.getlist("love")
    )  # 不会覆盖love的值，会返回列表的形式 # ['youxi', 'xuexi', 'yundong']

    return HttpResponse("ok")


# 获取请求体
def getRequestBody(request):

    # 在各种http请求方法中，POST/PUT/PATCH都是可以设置请求体的。
    # request.POST 中获取客户端通过POST发送过来的请求体，无法获取PUT/PATCH的请求体。
    # 请求体内容
    """ POST 请求 (只接受表单格式的数据，不接受json格式的数据)
        curl --location 'localhost:8001/users/body/?password=123' \
        --form 'name="lihua"' \
        --form 'love="youxi"' \
        --form 'love="yundong"'
    """
    print(request.POST)  # 显示的请求体内容 # <QueryDict: {'asdf': ['asdf']}>
    print(request.POST.get("name"))  # lihua
    print(request.POST.getlist("love"))  # ['youxi', 'yundong']
    print(request.GET)  # 也可以接受get的请求参数 # <QueryDict: {'password': ['123']}>

    """ PUT / PATCH 请求 (不接受form表单的形式发送数据, 只接受json格式的数据)
        curl --location --request PUT 'localhost:8001/users/body/?password=123' \
        --header 'Content-Type: application/json' \
        --data '{
            "name": "lihua",
            "love": ["youxi", "yundong"]
        }'
    """
    # 使用 request.body 获取请求体数据 可以接受 POST / PUT / PATCH
    print(
        request.body
    )  # 字节数据 # b'{\n    "name": "lihua",\n    "love": ["youxi", "yundong"]\n\n}'
    # #接受客户端发送的json格式
    import json

    data = json.loads(request.body)
    print(data)  # {'name': 'lihua', 'love': ['youxi', 'yundong']}

    return HttpResponse("ok")


# 获取请求头数据


def getHeaderData(request):
    # 获取请求头数据
    print(request.META)  # 获取原生请求头
    # 获取包括系统环境，客户端环境和 http 请求的请求头等元信息
    #     'SERVER_NAME': 'ubuntu'     # 服务端的系统名
    #     'SERVER_PORT': '8001'       # 服务端的端口
    #     'REMOTE_HOST': ''           # 客户端的所在IP地址，有时候可能是域名
    #     'REQUEST_METHOD': 'POST'    # 客户端本次请求时的http请求方法
    #     'PATH_INFO': '/users/meta/' # 客户端本次请求时的url路径
    #     'REMOTE_ADDR': '127.0.0.1'  # 客户端的所在IP地址
    #     'CONTENT_TYPE': 'application/json # 客户端本次请求时的数据MIME格式
    #

    print(request.headers)
    # 获取 http请求的请求头
    # {
    #     "Content-Length": "57",
    #     "Content-Type": "application/json",
    #     "User-Agent": "PostmanRuntime/7.37.3",
    #     "Accept": "*/*",
    #     "Postman-Token": "5f83d490-7aee-4014-bab9-8bfb423cc271",
    #     "Host": "localhost:8001",
    #     "Accept-Encoding": "gzip, deflate, br",
    #     "Connection": "keep-alive",
    # }

    # 获取自定义请求头, 两种方式
    print(request.META.get("HTTP_MYHEADER")) # xxyyxx， 不推荐使用
    print(request.headers.get("myheader")) # xxyyxx
    return HttpResponse("ok")

# 上传文件
def getFile(request):
    # 获取上传文件，可以接收多个文件
    print(request.FILES) # 只能接受POST 请求上传的文件，其他请求不可以
    # <MultiValueDict: {'file': [<InMemoryUploadedFile: aa.txt (text/plain)>]}>


    print(request.FILES.get("file")) # aa.txt
    file = request.FILES.get("file")
    print(file, type(file)) # aa.txt <class 'django.core.files.uploadedfile.InMemoryUploadedFile'>

    files = request.FILES.getlist("file")
    print(files) # [<InMemoryUploadedFile: aa.txt (text/plain)>, <InMemoryUploadedFile: init.sh (application/x-sh)>]

    for file in request.FILES.getlist("file"):
        with open(f'./{file.name}', 'wb') as f: # 当前路径
            f.write(file.read()) # 写入文件操作
    return HttpResponse("ok")