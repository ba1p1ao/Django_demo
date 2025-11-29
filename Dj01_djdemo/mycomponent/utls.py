from django.urls import path
from mycomponent import views

urlpatterns = [
    path("software/", views.SoftwareView.as_view()),
    # 分页
    path("page/", views.PageView.as_view()),

    # 函数试图缓存
    path("funccache/", views.funccache),

    # 类视图缓存
    path("methodcache/", views.CacheView.as_view()),

    # 缓存API
    path("apicache/", views.APICacheView.as_view()),
]
