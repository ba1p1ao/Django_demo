from rest_framework import serializers
from apps.order.models import Order, OrderGoods
from apps.goods.models import Goods
from muxishop.settings import IMAGE_URL


class OrderGoodsSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderGoods
        fields = "__all__"


class OrderSerializer(serializers.ModelSerializer):

    def create(self, validated_data):
        # validated_data["is_delete"] = 0
        # validated_data["pay_status"] = 0
        # validated_data["create_time"] = datetime.now().strftime("%Y-%m-%d %x")
        order = Order.objects.create(**validated_data)
        return order

    class Meta:
        model = Order
        fields = "__all__"


class OrderManyGoodsSerializer(serializers.Serializer):
    email = serializers.CharField(required=True)
    trade_no = serializers.CharField(required=True)
    order_amount = serializers.DecimalField(max_digits=10, decimal_places=2)
    address_id = serializers.IntegerField()
    pay_status = serializers.CharField(required=True)
    pay_time = serializers.DateTimeField()
    ali_trade_no = serializers.CharField()
    is_delete = serializers.IntegerField()
    create_time = serializers.DateTimeField("%Y-%m-%d %H:%M:%S")

    order_goods = serializers.SerializerMethodField()

    def get_order_goods(self, obj):
        # 查询该 trade_no 的 order_goods 信息
        order_goods = OrderGoods.objects.filter(trade_no=obj.trade_no).all()
        # 调用 OrderGoodsSerializer 对 order_goods 进行序列化
        ser_data = OrderGoodsSerializer(instance=order_goods, many=True).data

        for ser in ser_data:
            sku_id = ser.get("sku_id")
            goodinfo = Goods.objects.filter(sku_id=sku_id).values("name", "image", "p_price", "shop_name").first()
            if goodinfo:
                # ser_goodinfo = GoodsSerializer(instance=goodinfo).data
                ser["name"] = goodinfo["name"]
                ser["image"] = IMAGE_URL + goodinfo["image"]
                ser["p_price"] = goodinfo["p_price"]
                ser["shop_name"] = goodinfo["shop_name"]
        return ser_data

    class Meta:
        model = Order
        fields = "__all__"
