from rest_framework import serializers
from apps.cart import models


class CartSerializer(serializers.ModelSerializer):
    
    email = serializers.CharField(required=True)
    sku_id = serializers.CharField(required=True)

    class Meta:
        model = models.Cart
        fields = "__all__"
