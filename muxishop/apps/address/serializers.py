from rest_framework import serializers
from apps.address import models


class UserAddressSerializer(serializers.ModelSerializer):
    email = serializers.CharField(required=True, allow_blank=False)
    signer_name = serializers.CharField(required=True, allow_blank=False)
    telphone = serializers.CharField(required=True, allow_blank=False)
    signer_name = serializers.CharField(required=True, allow_blank=False)
    signer_address = serializers.CharField(required=True, allow_blank=False)
    district = serializers.CharField(required=True, allow_blank=False)
    

    class Meta:
        model = models.UserAddress
        fields = "__all__"
