from django.urls import path, re_path
from repath import views

# 导入自定义的转换器
from repath import converter

app_name = "repath"

urlpatterns = [

    #path("url路径,视图函数/视图类，name="路径别名")
    path("index/", views.index),

    # 正则路由
    #re_path(r"^url路径/(?P<参数变量名>正则模式)/$"，视图函数/视图类)，
    re_path(r"^user/(?P<uid>\d+)/$", views.get_id), 
    re_path(r"^user/(?P<uname>[a-zA-Z]+)/(?P<uage>\d+)/$", views.get_info),


    # path 内置路由转换器 包含 (str, int, uuid, slug, path)

    # str: 匹配除了'"之外的非空字符串。如果表达式内不包含转换器，则会默认匹配字符串。str -
    # int: 匹配0 或任何正整数。返回-个 int 。
    # slug: 匹配任意由 ASCI| 字母或数字以及连字符和下划线组成的短标签。比如，building-your-1st-django_site 。
    # uuid: 匹配一个格式化的 UUID。为了防止多个 URL 映射到同一个页面，必须包含破折号并且字符都为小写。比如，d3-6885-
    #       417e-a8a8-6c931e272f00。返回-个 UUID 实例。
    # path: 匹配非空字段，包括路径分隔符'""。它允许你匹配完整的 URL路径而不是像 str 那样匹配 URL 的一部分。


    # path("user/<int:number>/", views.get_number), # 路由是有上到下一次识别，\d+ 包含 int 优先匹配 \d+
    path("rev/<int:number>/", views.get_number),
    path("rev/<uuid:uuid>/", views.get_uuid), # 如果路由中同时存在 str 与 uuid ，uuid要写在前面，否则 str 会优先捕获
    path("rev/<str:like>/", views.get_like),
    
    # 使用自定义的路由转换器 
    path("rev2/<moble:moble>/", views.get_moble)
]