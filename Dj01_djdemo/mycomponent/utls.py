from django.urls import path
from mycomponent import views

urlpatterns = [
    path("software/", views.SoftwareView.as_view()),
    # 分页
    path("page/", views.PageView.as_view()),
]
