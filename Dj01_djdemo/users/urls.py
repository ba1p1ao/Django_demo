from django.urls import path
from users import views

urlpatterns = [
    path("index/", views.index),
    path("users/", views.users),
]