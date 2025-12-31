from email.policy import default
from idlelib.rpc import request_queue

from django.http import HttpResponse
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import (
    CreateModelMixin,
    RetrieveModelMixin,
    UpdateModelMixin,
    DestroyModelMixin,
    ListModelMixin
)
from apps.address.serializers import UserAddressSerializer
from apps.address import models
from utils.JWTAuth import JWTQueryParamAuthentication, JWTHeaderQueryParamAuthentication
from utils.ResponseMessage import AddressResponse
from datetime import datetime


# 使用 mixins 封装的create，update，get，delete
class UserAddressGenericAPIView(
    GenericAPIView,
    CreateModelMixin,
    RetrieveModelMixin,
    UpdateModelMixin,
    DestroyModelMixin,
    ListModelMixin
):
    queryset = models.UserAddress.objects
    serializer_class = UserAddressSerializer
    authentication_classes = [JWTHeaderQueryParamAuthentication, ]

    def get(self, request):
        if not request.user.get("status"):
            return AddressResponse.failed("用户信息已过期，请重新登录")
        email = request.user.get("payload").get("email")
        # print(email)
        addresses = self.get_queryset().filter(email=email).order_by("-default", "create_time")

        # 判断是否存在默认地址，如果没有默认地址，将最近修改的地址改为默认地址
        if not addresses.filter(default=True).exists():
            first_address = addresses.first()
            if first_address:
                first_address.default = True
                first_address.save()
                addresses = self.get_queryset().filter(email=email).order_by("-default", "create_time")

        response_data = UserAddressSerializer(instance=addresses, many=True).data
        # print(response_data)
        return AddressResponse.success(response_data)

    def post(self, request):
        if not request.user.get("status"):
            return AddressResponse.failed("用户信息已过期，请重新登录")
        email = request.user.get("payload").get("email")
        address_count = self.get_queryset().filter(email=email).count()
        if address_count + 1 > 25:
            return AddressResponse.failed("最多只能设置 25 个地址")
        request_data = request.data
        request_data["email"] = email
        if request_data["default"]:
            # 如果用户设置了默认地址，先将原来的默认地址修改
            self.get_queryset().filter(email=email, default=1).update(default=0)
            request_data["default"] = 1
        else:
            request_data["default"] = 0

        if not (request_data["signer_name"] or
                request_data["telphone"] or
                request_data["signer_address"] or
                request_data["district"]):
            return AddressResponse.failed("参数不能为空")

        self.get_queryset().create(**request_data)
        return AddressResponse.success("添加成功")

    def delete(self, request):
        if not request.user.get("status"):
            return AddressResponse.failed("用户信息已过期，请重新登录")
        email = request.user.get("payload").get("email")
        delete_address_id = request.data.get("id")
        address = self.get_queryset().filter(id=delete_address_id, email=email)
        if not address:
            return AddressResponse.failed("该地址信息不存在，请刷新页面或重新登录")
        address.delete()
        return AddressResponse.success("删除成功")


# 使用 mixins 中的 ListModelMixin
class UserAddressListGenericAPIView(GenericAPIView, ListModelMixin):
    queryset = models.UserAddress.objects
    serializer_class = UserAddressSerializer
    authentication_classes = [JWTQueryParamAuthentication, ]  # 用来做 token 认证

    # authentication_classes 优点就是，在调用类中的每一个函数，都是去做 token 认证
    # 在 request 中 添加字段 user，auth，
    # request.user：JWTQueryParamAuthentication.authenticate() 方法返回的第一个值，result，用户信息
    # request.auth：JWTQueryParamAuthentication.authenticate() 方法返回的第二个值，token，token信息

    # 返回所有数据
    def get(self, request):
        return self.list(request)


class UserAddressEditGenericAPIView(GenericAPIView, UpdateModelMixin):
    queryset = models.UserAddress.objects
    serializer_class = UserAddressSerializer

    def post(self, request):
        # print(request.data)
        if not request.user.get("status"):
            return AddressResponse.failed("用户信息已过期，请重新登录")
        email = request.user.get("payload").get("email")
        request_data = request.data
        request_data["email"] = email
        if request_data.get("default"):
            # 如果用户设置了默认地址，先将原来的默认地址修改
            self.get_queryset().filter(email=email, default=1).update(default=0)
            request_data["default"] = 1
        else:
            request_data["default"] = 0

        try:
            address = self.get_queryset().get(id=request_data['id'], email=email)
            ser_data = self.get_serializer(address, data=request_data, partial=True)
            if ser_data.is_valid():
                ser_data.save()
                return AddressResponse.success("更新成功")
            else:
                return AddressResponse.failed(f"数据验证失败")
        except models.UserAddress.DoesNotExist:
            return AddressResponse.failed("地址信息不存在")


class UserAddressDefaultGenericAPIView(GenericAPIView):
    queryset = models.UserAddress.objects
    serializer_class = UserAddressSerializer

    def post(self, request):
        if not request.user.get("status"):
            return AddressResponse.failed("用户信息已过期，请重新登录")
        email = request.user.get("payload").get("email")

        # 将原默认地址取消
        self.get_queryset().filter(email=email, default=1).update(default=0)
        # 设置新的默认地址
        set_default_address_id = request.data.get("id")
        updated_count = self.get_queryset().filter(email=email, id=set_default_address_id, default=0).update(default=1)
        if updated_count == 0:
            return AddressResponse.failed("地址信息不存在，请重新添加")
        return AddressResponse.success("修改成功")
