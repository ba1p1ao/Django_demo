from django.urls import path
from apps.tools import views

urlpatterns = [
    path("captcha/", views.CaptchaCodeAPIView.as_view()),
    path("captcha/verify/", views.CaptchaVerifyAPIView.as_view()),
]