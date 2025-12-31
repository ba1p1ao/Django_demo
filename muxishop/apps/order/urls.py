from django.urls import path, re_path
from apps.order import views


urlpatterns = [
    path("", views.OrderGenericAPIView.as_view()),
    re_path(r"(?P<trade_no>.*)/$", views.OrderManyGoodsGenericAPIView.as_view()),
]