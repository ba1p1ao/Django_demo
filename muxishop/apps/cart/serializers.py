from rest_framework import serializers
from apps.cart.models import Cart


class CartSerializer(serializers.ModelSerializer):
    email = serializers.CharField(required=True)
    sku_id = serializers.CharField(required=True)

    class Meta:
        model = Cart
        fields = "__all__"


from apps.goods.models import Goods
from apps.goods.serializers import GoodsSerializer


class CartDetailSerializer(serializers.Serializer):
    email = serializers.CharField(required=True)
    sku_id = serializers.CharField(required=True)
    is_delete = serializers.IntegerField()
    nums = serializers.IntegerField()

    # 查询商品信息
    # SerializerMethodField() 会将 get_goods方法的返回值给goods
    goods = serializers.SerializerMethodField()

    # 因为 goods = serializers.SerializerMethodField() 调用了这个方法，
    # 所以需要创建 get_goods 这个方法，来给 goods 赋值
    def get_goods(self, obj):
        # obj 是 调用这个序列化器时，传进来的对象，这里就是Cart
        # 查询符合掉件的goods
        goods = Goods.objects.filter(sku_id=obj.sku_id).first()
        # 调用 goods 的序列化器
        ser_data = GoodsSerializer(instance=goods).data

        return ser_data
