from django.urls import path
from mytemplate import views

app_name = "template"
urlpatterns = [

    path("index/", views.index),
]