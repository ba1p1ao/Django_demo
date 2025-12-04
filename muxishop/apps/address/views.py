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


# 使用 mixins 封装的create，update，get，delete
class UserAddressGenericAPIView(
    GenericAPIView,
    CreateModelMixin,
    RetrieveModelMixin,
    UpdateModelMixin,
    DestroyModelMixin
):
    queryset = models.UserAddress.objects
    serializer_class = UserAddressSerializer
    authentication_classes = [JWTHeaderQueryParamAuthentication, ]

    def post(self, request):
        return self.create(request)

    def get(self, request, pk):
        return self.retrieve(request, pk=pk)

    def put(self, request, pk):
        if not request.user['status']:
            return HttpResponse(request.user['error'])
        return self.update(request)

    def delete(self, request, pk):
        if not request.user['status']:
            return HttpResponse(request.user['error'])
        return self.destroy(request)


# 使用 mixins 中的 ListModelMixin
class UserAddressListGenericAPIView(GenericAPIView, ListModelMixin):
    queryset = models.UserAddress.objects
    serializer_class = UserAddressSerializer
    authentication_classes = [JWTQueryParamAuthentication, ] # 用来做 token 认证
    # authentication_classes 优点就是，在调用类中的每一个函数，都是去做 token 认证
    # 在 request 中 添加字段 user，auth，
    # request.user：JWTQueryParamAuthentication.authenticate() 方法返回的第一个值，result，用户信息
    # request.auth：JWTQueryParamAuthentication.authenticate() 方法返回的第二个值，token，token信息

    # 返回所有数据
    def get(self, request):
        return self.list(request)
