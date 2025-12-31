from rest_framework import serializers
from apps.goods import models
from muxishop.settings import IMAGE_URL


class GoodsSerializer(serializers.ModelSerializer):
    # 这里边写的字段就是你想要进行序列化时处理的字段

    image = serializers.SerializerMethodField()

    def get_image(self, obj):
        new_image_url = IMAGE_URL + obj.image
        return new_image_url

    class Meta:
        model = models.Goods
        fields = "__all__"


class GoodsSearchSerializer(serializers.ModelSerializer):
    """商品搜索专用序列化器，包含评论数量"""
    comment_count = serializers.IntegerField(read_only=True)
    image = serializers.SerializerMethodField()

    def get_image(self, obj):
        return IMAGE_URL + obj.image

    class Meta:
        model = models.Goods
        fields = ['sku_id', 'name', 'p_price', 'shop_name', 'image', 'comment_count']
