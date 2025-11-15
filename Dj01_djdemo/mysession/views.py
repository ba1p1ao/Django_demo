from django.shortcuts import render
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