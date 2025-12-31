from django.urls import path
from apps.pay.views import ToAliPayPageAPIView, AlipayAPIView

urlpatterns = [
    path("alipay/", ToAliPayPageAPIView.as_view()),
    path("alipay/return/", AlipayAPIView.as_view()),
]
