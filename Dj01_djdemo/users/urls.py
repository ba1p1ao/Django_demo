from django.urls import path
from users import views

urlpatterns = [
    path("index/", views.index),
    path("users/", views.users),
    path("args/", views.getAllargs),
    path("body/", views.getRequestBody),
    path("meta/", views.getHeaderData),
    path("file/", views.getFile),

]