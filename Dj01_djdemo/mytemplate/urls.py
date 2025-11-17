from django.urls import path
from mytemplate import views

app_name = "template"
urlpatterns = [

    path("index/", views.index),
    path("template/", views.get_template),
    path("iffor/", views.iffor),
    path("myfilter/", views.myfilter),
    path("temfenli/", views.tem_fenli),
    path("temjichengusers/", views.tem_jicheng_users),
    path("temjichenggoods/", views.tem_jicheng_goods),
    path("temjichenginfo/", views.tem_jicheng_info),

]