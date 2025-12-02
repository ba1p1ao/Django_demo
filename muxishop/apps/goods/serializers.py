from rest_framework import serializers
from apps.goods import models
from muxishop.settings import IMAGE_URL


class GoodsSerializer(serializers.ModelSerializer):
    # 这里边写的字段就是你想要进行序列化时处理的字段

    image = serializers.SerializerMethodField()
    create_time = serializers.DateTimeField('%Y-%m-%d %X')

    def get_image(self, obj):
        new_image_url = IMAGE_URL + obj.image
        return new_image_url

    class Meta:
        model = models.Goods
        fields = "__all__"


    