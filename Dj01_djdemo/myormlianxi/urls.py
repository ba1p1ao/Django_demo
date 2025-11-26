from django.urls import path
from myormlianxi.views import *

app_name = "ormlianxi"

urlpatterns = [
    path("book/", BookView.as_view())
]