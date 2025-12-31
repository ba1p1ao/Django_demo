from django.urls import path
from apps.user import views


urlpatterns = [
    path("", views.UserRegisterAPIView.as_view()),
    path("register/", views.UserExistAPIView.as_view()),
    path("login/", views.UserLoginView.as_view()),
    path("info/", views.UserInfoAPIView.as_view()),
    path("password/", views.UpdateUserPasswordAPIView.as_view()),
]