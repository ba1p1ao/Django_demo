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

    def post(self, request):
        return self.create(request)

    def get(self, request, pk):
        return self.retrieve(request)

    def put(self, request, pk):
        return self.update(request)

    def delete(self, request, pk):
        return self.destroy(request)

# 使用 mixins 中的 ListModelMixin
class UserAddressListGenericAPIView(GenericAPIView, ListModelMixin):
    queryset = models.UserAddress.objects
    serializer_class = UserAddressSerializer

    # 返回所有数据
    def get(self, request):
        return self.list(request)
