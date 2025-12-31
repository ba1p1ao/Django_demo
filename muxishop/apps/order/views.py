from django.http import HttpResponse, JsonResponse
from django.db import transaction
from rest_framework.generics import GenericAPIView
from apps.order.models import Order, OrderGoods
from apps.cart.models import Cart
from apps.order.serializers import OrderGoodsSerializer, OrderSerializer, OrderManyGoodsSerializer
from utils.ResponseMessage import OrderResponse
from django.utils import timezone
import time


class OrderManyGoodsGenericAPIView(GenericAPIView):
    # queryset = OrderGoods.objects
    # serializer_class = OrderGoodsSerializer
    # def post(self, request):
    #     # 序列化 json 转 obj
    #     #  elf.get_serializer() 获取序列化对象 OrderGoodsSerializer
    #     order_goods_obj = self.get_serializer(data=request.data)
    #     order_goods_obj.is_valid(raise_exception=True)
    #     order_goods_obj.save()
    #
    #     return HttpResponse("ok")

    # def get(self, request):
    #     # self.get_queryset() 就是 获取上面写的 models.OrderGoods.objects
    #     return HttpResponse(self.get_serializer(instance=self.get_queryset(), many=True).data)

    queryset = Order.objects
    serializer_class = OrderManyGoodsSerializer

    def get(self, request, trade_no):
        if not request.user.get("status"):
            return OrderResponse.failed("用户认证过期，请重新登录", safe=False)
        email = request.user.get("payload").get("email")
        db_result = self.get_queryset().filter(email=email, is_delete=0, trade_no=trade_no).first()
        data = self.get_serializer(instance=db_result, many=False).data
        return OrderResponse.success(data)


class OrderGenericAPIView(GenericAPIView):
    queryset = Order.objects
    serializer_class = OrderSerializer

    @transaction.atomic
    def post(self, request):
        if not request.user.get("status"):
            return OrderResponse.failed("用户认证过期，请重新登录", safe=False)
        # print(request.data)
        request_data = request.data
        email = request.user.get("payload").get("email")
        trade_no = int(time.time() * 1000)
        # 创建订单数据
        try:
            trade_data = request_data["trade"]
            trade_data["trade_no"] = trade_no
            trade_data["email"] = email
            # 这里需要添加支付状态，默认为0
            trade_data["pay_status"] = 0
            trade_data["is_delete"] = 0
            # trade_data["create_time"] = timezone.now()
            # 创建商品数据
            goods_data = request_data["goods_list"]
            # print(trade_data)
            trade_data_ser = self.get_serializer(data=trade_data)
            if not trade_data_ser.is_valid():
                return OrderResponse.failed("trade 数据验证失败")

            trade_data_ser.save()

            # 批量创建订单商品
            order_goods_list = []
            for goods in goods_data:
                # print(goods)
                order_goods_list.append(
                    OrderGoods(
                        trade_no=trade_no,
                        sku_id=goods["sku_id"],
                        goods_num=goods["nums"]
                    )
                )
            # 批量添加
            OrderGoods.objects.bulk_create(order_goods_list)
            # 批量更新购物车
            Cart.objects.filter(sku_id__in=[g["sku_id"] for g in goods_data], email=email).update(is_delete=1)
        except Exception as e:
            print(e)
            return OrderResponse.failed(f"订单创建失败")

        return OrderResponse.success(trade_data_ser.data)

    def get(self, request):
        if not request.user.get("status"):
            return OrderResponse.failed("用户认证过期，请重新登录", safe=False)
        email = request.user.get("payload").get("email")
        pay_status = request.GET.get("pay_status")
        if pay_status == "-1":
            db_data = self.get_queryset().filter(email=email, is_delete=0).order_by("-create_time")
        else:
            db_data = self.get_queryset().filter(email=email, is_delete=0, pay_status=pay_status).order_by(
                "-create_time")

        ser_data = OrderManyGoodsSerializer(instance=db_data, many=True).data

        return OrderResponse.success(ser_data)

    def delete(self, request):
        if not request.user.get("status"):
            return OrderResponse.failed("用户认证过期，请重新登录", safe=False)
        email = request.user.get("payload").get("email")
        trade_no = request.data.get("trade_no")

        updated_count = self.get_queryset().filter(
            email=email,
            trade_no=trade_no,
            is_delete=0
        ).update(is_delete=1)

        if updated_count == 0:
            return OrderResponse.failed("订单号不存在，请刷新页面")

        return OrderResponse.success("删除成功")

    def put(self, request):
        if not request.user.get("status"):
            return OrderResponse.failed("用户认证过期，请重新登录", safe=False)
        email = request.user.get("payload").get("email")
        trade_no = request.data.get("trade_no")
        updated_count = self.get_queryset().filter(email=email, trade_no=trade_no).update(**request.data)
        if updated_count == 0:
            return OrderResponse.failed("订单不存在或无权限修改", safe=False)
        return OrderResponse.success("更新成功", safe=False)
