from django.urls import path
from mytemplate import views

app_name = "template"
urlpatterns = [

    path("index/", views.index),
    path("template/", views.get_template),
    path("iffor/", views.iffor),
    path("myfilter/", views.myfilter),
]