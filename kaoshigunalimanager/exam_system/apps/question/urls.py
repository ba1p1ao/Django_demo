from django.urls import path
from apps.question import views


urlpatterns = [
    path("list/", views.QuestionListView.as_view()),

    path("add/", views.QuestionAddView.as_view()),
    path("batch/", views.QuestionDeleteListView.as_view()),
    path("<int:id>/", views.QuestionInfoView.as_view()),
]