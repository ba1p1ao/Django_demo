from django.urls import path
from apps.mistake import views

urlpatterns = [
    path("list-with-statistics/", views.MistakeListWithStatisticsView.as_view()),
]

