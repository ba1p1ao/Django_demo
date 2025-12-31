from django.urls import path
from apps.adminer import views


urlpatterns = [
    path("users/", views.UserListView.as_view()),
    path("users/statistics/", views.UserStatisticsView.as_view()),
    path("users/<int:user_id>/", views.UserInfoView.as_view()),
]