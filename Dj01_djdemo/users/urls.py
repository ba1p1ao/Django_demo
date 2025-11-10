from django.urls import path
from users import views

#使用路由反向解析 reverse 时, 
# 必须在当前子应用的路由文件中
# 设置 app_name 为当前子应用的包名
app_name = "users" # 为当前子应用的包名

urlpatterns = [
    path("index/", views.index),
    path("users/", views.users),
    path("args/", views.getAllargs),
    path("body/", views.getRequestBody),
    path("meta/", views.getHeaderData, name="meta"), # name 设置路径别名
    path("file/", views.getFile),
    path("reshtml/", views.getResponseHTML),
    path("resjson/", views.getResponseJSON),
    path("resfile/", views.getResponseFile),
    path("setheader/", views.setHeaders),
    path("zwredirect/", views.zhanWaiRedirect),
    path("znredirect/", views.zhanNeiRedirect, name="znredirect"), # name 设置路径别名
]