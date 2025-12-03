from django.urls import path, re_path
from apps.order import views


urlpatterns = [
    path("", views.OrderGoodsGenericAPIView.as_view()),
    re_path(r"(?P<trade_no>.*)/$", views.OrderGoodsGenericAPIView.as_view()),
]