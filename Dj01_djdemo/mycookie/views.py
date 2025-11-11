from django.http.response import HttpResponse


def set_cookie(request):
    """设置cookie"""
    response = HttpResponse("set_cookie")
    response.set_cookie("username", "lihua", max_age=30)  # max_age 有效时间，单位秒

    return response


def get_cookie(request):
    """获取cookie"""
    print(request.COOKIES)
    print(request.COOKIES.get("username"))
    return HttpResponse("get_cookie")


def del_cookie(request):
    """删除cookie"""
    response = HttpResponse("del_cookie")
    # 将 cookie 的有效时间设置成 0s 
    response.set_cookie("username", max_age=0)
    return response

from django.views.decorators.http import require_http_methods
from django.urls import reverse
from django.shortcuts import redirect
from django.http.response import HttpResponseRedirect

@require_http_methods(["GET"])
def login(request):
    """显示登录表单"""
    content = """
    <form action="/cookie/login_handle/" method="POST">
        登录账号：<input type="text" name="username"><br>
        登录密码：<input type="password" name="password"><br>
        <button>登录</button>
    </form>
    """
    return HttpResponse(content)


@require_http_methods(["POST"])
def login_handle(request):
    """处理登录信息"""
    username: str = request.POST.get("username")
    password: str = request.POST.get("password")

    if not username or not password:
        return HttpResponse("用户名和密码不能为空", status=400)
    
    # 到数据库中查询当前账号密码是否正确

    from hashlib import sha256
    sha = sha256()
    sha.update(password.encode())
    password_hash = sha.hexdigest()
    # 123 hash a665a45920422f9d417e4867efdc4fb8a04a1f3fff1fa07e998e86f7f7a27ae3
    if username == 'admin' and password_hash == "a665a45920422f9d417e4867efdc4fb8a04a1f3fff1fa07e998e86f7f7a27ae3":
        # 登录成功, 跳转页面

        # 以 / 开头表示从网站根路径开始
        # 如果不是 / 开头表示相对路径，在当前路径的后面直接添加
        # response = HttpResponseRedirect("/cookie/info/") 

        # 使用 reverse (app_name : 路由 name)， 
        # # 使用 reverse() 是最安全的方式，因为它基于 URL 名称而不是硬编码的路径。

        # reverse() 注意事项
            # 命名空间 (cookie:) → 由总路由的 namespace 参数决定
            # URL 名称 (info) → 由子路由中 path() 的 name 参数决定
            # 子路由的 app_name 必须与总路由 namespace 保持一致
        response = HttpResponseRedirect(reverse("cookie:info")) 
        
        response.set_cookie("username", username)
        response.set_cookie("is_login", True, max_age=30)
    else:
        response = HttpResponseRedirect("/cookie/login/")
        response["method"] = "GET"
        response.set_cookie("status", "fail")

    return response



def info(request):
    print(request.COOKIES)
    print(request.COOKIES.get("username"))
    print(request.COOKIES.get("is_login"))
    # username = request.COOKIES.get("username")
    is_login = request.COOKIES.get("is_login")
    if not is_login:
        # redirect 内部调用了 reverse 来解析 URL 名称
        return redirect("cookie:login")
    return HttpResponse("info")