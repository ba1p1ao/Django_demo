from django.urls import path
from apps.goods import views


urlpatterns = [
    path("category/<int:category_id>/<int:page>/", views.GoodsCategoryAPIView.as_view()),
    path("find/", views.GoodsFindAPIView.as_view()),
    path("search/<str:keyword>/<int:page>/<int:order>/", views.GoodsSearchAPIView.as_view()),
    path("get_keyword_data_count/<str:keyword>/", views.GoodsKeywordDataCountView.as_view()),
    path("detail/<str:sku_id>/", views.GoodsDatilAPIView.as_view()),
]