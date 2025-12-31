from django.urls import path
from apps.cart import views

urlpatterns = [
    path("", views.CartAPIView.as_view()),
    path("detail/", views.CartDetailAPIView.as_view()),
    path("num/", views.UpdateCartNumberAPIView.as_view()),
    path("count/", views.CartCountAPIView.as_view()),
]