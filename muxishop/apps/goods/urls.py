from django.urls import path
from apps.goods import views


urlpatterns = [
    path("category/<int:category_id>/<int:page>/", views.GoodsCategoryAPIView.as_view()),
    path("<str:sku_id>/", views.GoodsDatilAPIView.as_view()),
]