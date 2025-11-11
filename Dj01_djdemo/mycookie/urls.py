from django.urls import path
from mycookie import views


app_name = "cookie"

urlpatterns = [
    path("get", views.get_cookie),
    path("set", views.set_cookie),
    path("del", views.del_cookie),

    # 模拟用户 登录，验证cookie
    path("login/", views.login, name="login"),
    path("login_handle/", views.login_handle),
    path("info/", views.info, name="info"),
]
