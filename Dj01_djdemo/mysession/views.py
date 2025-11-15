from django.shortcuts import redirect, render
from django.http import HttpResponse, HttpRequest

# Create your views here.

def set_session(request: HttpRequest):
    # 设置session
    request.session["name"] = "lihua"
    request.session["id"] = 101

    # 设置有效时间 5s，推荐直接在 settings.py 里面写 SESSION_COOKIE_AGE = 时间
    request.session.set_expiry(5)
    return HttpResponse("set_session")


def get_session(request: HttpRequest):
    # 获取session

    # 提取单个session
    print(request.session.get("name"))
    print(request.session.get("id"))

    # 获取全部session
    print(request.session.items())
    
    # session 过期时间默认14天 1209600秒
    print(request.session.get_expiry_date())
    print(request.session.get_expiry_age())
    return HttpResponse(request.session.items())


def del_session(request: HttpRequest):
    # 删除session

    # # 删除 session 中的某一个值， 需要判断是否存在，或者抛出异常
    if request.session.get("name"):
        request.session.pop("name")

    # try:
    #     request.session.pop("name")
    # except Exception as e:
    #     print(e)

    # 删除所有session

    request.session.clear()

    return HttpResponse("del_session") 



from django.views.decorators.http import require_http_methods



@require_http_methods(["GET"])
def login(request: HttpRequest):
    """显示登录表单"""
    content = """
    <form action="/session/login_handle/" method="POST">
        登录账号：<input type="text" name="username"><br>
        登录密码：<input type="password" name="password"><br>
        <button>登录</button>
    </form>
    """
    return HttpResponse(content)


@require_http_methods(["POST"])
def login_handle(request: HttpRequest):
    username = request.POST.get("username")
    password = request.POST.get("password")
    # 这里可以对password进行加密
    if username == 'admin' and password == "admin":
        request.session["username"] = username
        request.session["is_login"] = True
        request.session.set_expiry(10)
        return redirect("/session/info/")
    

@require_http_methods(["GET"])
def info(request: HttpRequest):
    is_login = request.session.get("is_login")
    if is_login:
        username = request.session.get("username")
        return HttpResponse(f"hello {username}")
    else:
        return redirect("/session/login/")







