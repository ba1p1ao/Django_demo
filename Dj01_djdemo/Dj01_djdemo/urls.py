"""
URL configuration for Dj01_djdemo project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

# from django.contrib import admin
# from django.urls import path
# from goods import views as goodsViews

# urlpatterns = [
#     path('admin/', admin.site.urls),
#     path("index/", goodsViews.index, name="goods"),
#     path("goods/", goodsViews.goods, name="goods"),
# ]

from django.contrib import admin
from django.urls import path, include

# 路由分层
# 主项目的urls为主路由，include可以添加子路由
urlpatterns = [
    path("admin/", admin.site.urls),
    path("goods/", include("goods.urls")), # 添加前缀， localhost:8000/goods/ + goods 的路由

    # 路由前缀的别名，也叫命名空间, 
    # namespace 是include 里面的，不是path里面的参数
    # 填写 namespace 方便于 reverse 做站内跳转
    path("users/", include("users.urls", namespace="users")),

    # 添加 mycookie应用 路由
    path("cookie/", include("mycookie.urls", namespace="cookie")),
    path("session/", include("mysession.urls", namespace="session")),
    path("repath/", include("repath.urls", namespace="repath")),
    path("template/", include("mytemplate.urls", namespace="template")),
    path("cbv/", include("mycbv.urls", namespace="cbv")),
    path("student/", include("student.urls", namespace="student")),
]
