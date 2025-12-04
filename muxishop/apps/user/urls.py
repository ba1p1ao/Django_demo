from django.urls import path
from apps.user import views


urlpatterns = [
    path("", views.UserRegisterAPIView.as_view()),
    path("login/", views.UserLoginView.as_view()),
]