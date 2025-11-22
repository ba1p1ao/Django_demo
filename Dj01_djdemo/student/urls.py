from django.urls import path
from student.views import StudentView, StudentSearchView


app_name = "student"
urlpatterns = [
    path("list/", StudentView.as_view()),
    path("search/", StudentSearchView.as_view()),
]