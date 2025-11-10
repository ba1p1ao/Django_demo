from django.urls import path
from goods import views

# goods/urls.py, 为子路由
urlpatterns = [
    path("goods/", view=views.goods),
    path("index/", view=views.index),
]