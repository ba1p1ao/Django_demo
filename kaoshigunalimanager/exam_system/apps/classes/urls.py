from django.urls import path
from apps.classes import views


urlpatterns = [
    path("options/", views.ClassOptionView.as_view()),
    path("list/", views.ClassListView.as_view()),
]