from rest_framework import serializers
from apps.order import models

class OrderGoodsSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.OrderGoods
        fields = "__all__"