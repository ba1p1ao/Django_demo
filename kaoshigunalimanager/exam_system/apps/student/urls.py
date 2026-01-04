from django.urls import path
from apps.student import views


urlpatterns = [
    path("score/trend/", views.ScoreTrendView.as_view()),
    path("class/", views.StudentClassView.as_view()),
]