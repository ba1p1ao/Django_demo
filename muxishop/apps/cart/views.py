from django.http import HttpRequest
from django.shortcuts import render
from rest_framework.views import APIView
from apps.cart import models
from utils.ResponseMessage import CartResponse
from apps.cart.serializers import CartSerializer


class CartAPIView(APIView):
    # 先做用户权限认证
    
    # 修改或者添加购物车数据
    def post(self, request: HttpRequest):
        request_data = request.data
        print("request_data", request_data)
        email = request_data.get("email")
        sku_id = request_data.get("sku_id")
        nums = request_data.get("nums")

        cart = models.Cart.objects.filter(
            email=email, sku_id=sku_id, is_delete=0,
        ).first()

        # 存在则更新数据
        if cart:
            # 修改数量
            cart.nums += nums
            # 保存数据
            cart.save()
        else:
            request_data["is_delete"] = 0 # 添加字段
            # 反序列化
            new_cart_data = CartSerializer(data=request_data)
            # 需要对数据进行校验
            new_cart_data.is_valid()
            # print(new_cart_data)
            cart = models.Cart.objects.create(**new_cart_data.data)

        result = CartSerializer(instance=cart).data
        return CartResponse.success(result, safe=False)




