import decimal
import json
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.conf import settings
from django.db import connection
from django.db.models import Count, Q, F, OuterRef, Subquery
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, RetrieveAPIView
from apps.goods.models import Goods
from apps.comment.models import Comment
from utils.ResponseMessage import GoodsResponse
from utils.PageCache import page_cache
from datetime import datetime
from apps.goods.serializers import GoodsSerializer, GoodsSearchSerializer


# 获取商品分类的接口
# 访问方式是:http://localhost:8001/qoods/category/category_id/page
# class GoodsCategoryAPIView(APIView):
#     def get(self, request: HttpRequest, category_id: int = None, page: int = 1):
#         # print(request.user)
#         # if not request.user.get('status'):
#         #     return JsonResponse(request.user, safe=False)
#         current_page = (page - 1) * 20
#         end_data_count = page * 20
#         if category_id:
#             goods = Goods.objects.filter(type_id=category_id)[
#                 current_page:end_data_count
#             ]
#         response_data = GoodsSerializer(instance=goods, many=True).data
#         # goods_list = []
#         # for good in goods:
#         #     goods_list.append(good.__str__())
#
#         return GoodsResponse.success(response_data, safe=False)
#

class GoodsCategoryAPIView(ListAPIView):
    queryset = Goods.objects
    serializer_class = GoodsSerializer

    @page_cache(timeout=300, key_prefix="goods_category")
    def get(self, request: HttpRequest, category_id: int = None, page: int = 1):
        current_page = (page - 1) * 20
        end_data_count = page * 20
        if category_id:
            goods = self.get_queryset().filter(type_id=category_id)[
                current_page:end_data_count
            ]
        response_data = self.get_serializer(instance=goods, many=True).data
        return GoodsResponse.success(response_data, safe=False)


# 获取单个商品详细的接口
# class GoodsDatilAPIView(APIView):
#     def get(self, request: HttpRequest, sku_id: str = ""):
#         if sku_id:
#             good = Goods.objects.get(sku_id=sku_id)
#
#         result = GoodsSerializer(instance=good).data
#         return GoodsResponse.success(result, safe=False)

class GoodsDatilAPIView(RetrieveAPIView):
    queryset = Goods.objects
    serializer_class = GoodsSerializer
    lookup_field = 'sku_id'

    @page_cache(timeout=900, key_prefix="goods_detail")
    def get(self, request, *args, **kwargs):
        good = self.get_object()
        result = self.get_serializer(instance=good).data
        return GoodsResponse.success(result, safe=False)


# class GoodsFindAPIView(APIView):
#     def get(self, request):
#         goods = Goods.objects.filter(find=1).all()
#         result = GoodsSerializer(instance=goods, many=True).data
#         return GoodsResponse.success(result, safe=False)
#
class GoodsFindAPIView(ListAPIView):
    queryset = Goods.objects
    serializer_class = GoodsSerializer

    @page_cache(timeout=600, key_prefix="goods_find")
    def get(self, request):
        goods = self.get_queryset().filter(find=1).all()
        result = GoodsSerializer(instance=goods, many=True).data
        return GoodsResponse.success(result, safe=False)


# class GoodsSearchAPIView(APIView):
#     def dict_fetchall(self, cursor):
#         desc = cursor.description
#         return [dict(zip([col[0] for col in desc], row)) for row in cursor.fetchall()]
#
#     def get(self, request, keyword: str, page, order):
#         order_by = {
#             1: "r.comment_count",
#             2: "g.p_price"
#         }
#         limit_page = (page - 1) * 15
#         sql = """
#         select r.comment_count, concat('{}', g.image) as image, g.name, g.p_price, g.shop_name, g.sku_id
#         from goods g
#         left join (
#             select count(c.sku_id) as comment_count, c.sku_id
#             from comment c
#             group by c.sku_id
#         ) r
#         on g.sku_id=r.sku_id
#         where g.name like "%{}%"
#         order by {} desc limit {},15
#         """.format(settings.IMAGE_URL, keyword, order_by[order], limit_page)
#
#         cursor = connection.cursor()
#         cursor.execute(sql)
#         res = self.dict_fetchall(cursor)
#         final_list = []
#         for i in res:
#             res_json = json.dumps(i, cls=DecimalEncoder, ensure_ascii=False)
#             final_list.append(res_json)
#         return GoodsResponse.success(final_list)
# class DecimalEncoder(json.JSONEncoder):
#     def default(self, o):
#         if isinstance(o, decimal.Decimal):
#             return float(o)
#         elif isinstance(o, datetime):
#             return o.strftime("%Y-%m-%d %H:%M:%S")

class GoodsSearchAPIView(APIView):
    def get(self, request, keyword: str, page, order):
        page_size = 15
        offset = (page - 1) * page_size

        order_mapping = {
            1: "-comment_count",
            2: "-p_price"
        }
        order_by = order_mapping.get(order, "-comment_count")
        # 使用子查询获取每个商品的评论数
        comment_count_subquery = Comment.objects.filter(
            sku_id=OuterRef("sku_id")
        ).values("sku_id").annotate(count=Count("id")).values("count")[:1]
        # ORM 查询
        queryset = Goods.objects.annotate(
            comment_count=Subquery(comment_count_subquery)
        ).filter(name__icontains=keyword).order_by(order_by)
        # 分页
        goods_list = queryset[offset:offset + page_size]

        ser_data = GoodsSearchSerializer(instance=goods_list, many=True).data
        return GoodsResponse.success(ser_data)





#
# class GoodsKeywordDataCountView(View):
#     def get(self, request, keyword):
#         goods_count = Goods.objects.filter(name__icontains=keyword).count()
#         return GoodsResponse.success(goods_count, safe=False)
# 修改为 APIView
class GoodsKeywordDataCountView(APIView):
    def get(self, request, keyword):
        goods_count = Goods.objects.filter(name__icontains=keyword).count()
        return GoodsResponse.success(goods_count, safe=False)
