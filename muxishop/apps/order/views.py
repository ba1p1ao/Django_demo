from django.http import HttpResponse, JsonResponse
from rest_framework.generics import GenericAPIView
from apps.order import models
from apps.order.serializers import OrderGoodsSerializer


class OrderGoodsGenericAPIView(GenericAPIView):
    queryset = models.OrderGoods.objects
    serializer_class = OrderGoodsSerializer

    def post(self, request):
        # 序列化 json 转 obj
        #  elf.get_serializer() 获取序列化对象 OrderGoodsSerializer
        order_goods_obj = self.get_serializer(data=request.data)
        order_goods_obj.is_valid(raise_exception=True)
        order_goods_obj.save()

        return HttpResponse("ok")

    def get(self, request):
        # self.get_queryset() 就是 获取上面写的 models.OrderGoods.objects
        return HttpResponse(self.get_serializer(instance=self.get_queryset(), many=True).data)

    lookup_field = "trade_no" # 按这个字段获取唯一数据
    def get(self, request, trade_no):

        print(trade_no)
        data = self.get_serializer(instance=self.get_object(), many=False).data
        print(data)
        return JsonResponse(data, safe=False)

