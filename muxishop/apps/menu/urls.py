from django.urls import path
from apps.menu import views


urlpatterns = [
    path("mainmenu/", views.GoodsMainMenuView.as_view()),
    path("submenu/", views.GoodsSubMenuView.as_view()),
]