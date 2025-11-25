from django.urls import path
from myorm.views import *

app_name = "orm"
urlpatterns = [
    path("student/", StudentView.as_view()),
    path("article/", ArticleView.as_view()),
    path("teacher/", TeacherView.as_view()),
    path("area/", AreaView.as_view()),
    path("people/", PeopleView.as_view()),
]
