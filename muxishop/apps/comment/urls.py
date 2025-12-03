from django.urls import path, re_path
from apps.comment import views

# 使用 viewsets 视图做路由分发，可以将多个请求路径，写到一个视图里面
urlpatterns = [
    path("", views.CommentGenericAPIView.as_view(
        {
            # "请求方法method": "采用什么动作action"
            "get": "getAll",
            "post": "add"
        }
    )),
    # 有参数
    re_path(r"(?P<pk>\d+)/$", views.CommentGenericAPIView.as_view(
        {
            "get": "getOne",
            "put": "updateOne",
            "delete": "deleteOne",
        }
    )),
]