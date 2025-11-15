from django.urls import path, re_path
from repath import views
app_name = "repath"

urlpatterns = [

    #path("url路径,视图函数/视图类，name="路径别名")
    path("index/", views.index),

    # 正则路由
    #re_path(r"^url路径/(?P<参数变量名>正则模式)/$"，视图函数/视图类)，
    re_path(r"^user/(?P<uid>\d+)/$", views.get_id), 
    re_path(r"^user/(?P<uname>[a-zA-Z]+)/(?P<uage>\d+)/$", views.get_info), 
]