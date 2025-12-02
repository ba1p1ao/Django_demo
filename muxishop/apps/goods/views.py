from django.http import HttpRequest
from django.shortcuts import render
from rest_framework.views import APIView
from apps.goods import models
from utils.ResponseMessage import GoodsResponse


# 获取商品分类的接口
# 访问方式是:http://localhost:8001/qoods/category/category_id/page
class GoodsCategoryAPIView(APIView):

    def get(self, request: HttpRequest, category_id=None, page=1):
        current_page = (page - 1) * 20
        end_data_count = page * 20
        if category_id:
            goods = models.Goods.objects.filter(type_id=category_id)[current_page:end_data_count]
        
        goods_list = []
        for good in goods:
            goods_list.append(good.__str__())

        
        return GoodsResponse.success(goods_list, safe=False)