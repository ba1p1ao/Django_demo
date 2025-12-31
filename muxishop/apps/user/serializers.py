from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from apps.user import models
from utils.PasswordEncode import hash_password
from datetime import datetime


class UserSerializer(serializers.ModelSerializer):
    # 这里边写的字段就是你想要进行序列化时处理的字段
    email = serializers.EmailField(
        required=True, allow_null=False,
        validators=[UniqueValidator(queryset=models.User.objects.all(), message="用户已经存在了")]
    )
    birthday = serializers.DateTimeField('%Y-%m-%d %X')
    # write_only=True 数据序列化的时候不会显示该字段
    password = serializers.CharField(write_only=True)
    mobile = serializers.CharField(
        required=True, allow_null=False,
        validators=[UniqueValidator(queryset=models.User.objects.all(), message="手机号已存在")]
    )
    create_time = serializers.DateTimeField(required=False, format='%Y-%m-%d %X')

    def create(self, validated_data):
        validated_data["password"] = hash_password(validated_data.get("password"))
        validated_data["create_time"] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        user = models.User.objects.create(**validated_data)
        return user


    class Meta:
        model = models.User
        fields = "__all__"
