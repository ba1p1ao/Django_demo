from django.urls import path
from student.views import StudentView


app_name = "student"
urlpatterns = [
    path("list/", StudentView.as_view()),
]