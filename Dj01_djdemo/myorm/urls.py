from django.urls import path
from myorm.views import *

app_name = "orm"
urlpatterns = [
    path("student/", StudentView.as_view()),
]
