from django.urls import path, re_path
from apps.address import views

urlpatterns = [
    path("", views.UserAddressGenericAPIView.as_view()),
    path("list/", views.UserAddressListGenericAPIView.as_view()),
    re_path(r"(?P<pk>\d+)/$", views.UserAddressGenericAPIView.as_view()),
]