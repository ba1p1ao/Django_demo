from django.urls import path, re_path
from apps.comment import views

# # 使用 viewsets 视图做路由分发，可以将多个请求路径，写到一个视图里面
# urlpatterns = [
#     path("", views.CommentGenericAPIView.as_view(
#         {
#             # "请求方法method": "采用什么动作action"
#             "get": "getAll",
#             "post": "add"
#         }
#     )),
#     path("count/", views.CommentGenericAPIView.as_view({
#         "get": "getCommentCountData"
#     })),
#     path("detail/", views.CommentGenericAPIView.as_view({
#         "get": "getGoodsCommentData"
#     })),
#     # 有参数
#     re_path(r"(?P<pk>\d+)/$", views.CommentGenericAPIView.as_view(
#         {
#             "get": "getOne",
#             "put": "updateOne",
#             "delete": "deleteOne",
#         }
#     )),
#
# ]

urlpatterns = [
    # ========== 标准 CRUD ==========
    # 获取评论列表、创建评论
    path("", views.CommentViewSet.as_view({
        'get': 'list',
        'post': 'create'
    })),

    # 获取单个评论、更新评论、删除评论
    path("<int:pk>/", views.CommentViewSet.as_view({
        'get': 'retrieve',
        'put': 'update',
        'delete': 'destroy'
    })),

    # ========== 自定义业务接口 ==========
    # 获取商品评论数量
    path('count/', views.CommentCountView.as_view()),

    # 获取商品评论列表（带分页）
    path('detail/', views.CommentListView.as_view()),
]