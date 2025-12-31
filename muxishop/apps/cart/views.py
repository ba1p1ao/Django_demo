from django.http import HttpRequest
from django.db.models import Sum
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, UpdateAPIView
from apps.cart import models
from utils.ResponseMessage import CartResponse
from apps.cart.serializers import CartSerializer, CartDetailSerializer


class CartAPIView(APIView):
    # 先做用户权限认证

    def _get_email_from_request_user(self, request):
        """从认证用户获取email"""
        # 假设你的User模型有email字段
        return request.user.get("payload").get("email")

    # 修改或者添加购物车数据
    def post(self, request: HttpRequest):
        # print(request.user)
        if not request.user.get("status"):
            return CartResponse.failed("登录状态已过期，请重新登录", safe=False)
        request_data = request.data
        # print("request_data", request_data)
        # email = request_data.get("email")
        email = self._get_email_from_request_user(request)
        # print(email)
        request_data['email'] = email
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
            return CartResponse.success("添加成功", safe=False)
        else:
            request_data["is_delete"] = 0  # 添加字段
            # 反序列化
            new_cart_data = CartSerializer(data=request_data)
            # 需要对数据进行校验
            if new_cart_data.is_valid():
                # print(new_cart_data)
                cart = models.Cart.objects.create(**new_cart_data.data)
                return CartResponse.success("添加成功", safe=False)
            else:
                return CartResponse.failed("添加失败")

    def delete(self, request: HttpRequest):
        if not request.user.get("status"):
            return CartResponse.failed("登录状态已过期，请重新登录", safe=False)
        request_data = request.data
        email = self._get_email_from_request_user(request)
        sku_ids = request_data.get("sku_id")
        # 查询未删除的合法数据
        # for sku_id in sku_ids:
        #     carts = models.Cart.objects.filter(email=email, sku_id=sku_id, is_delete=0).first()
        #     if carts:
        #         carts.is_delete = 1
        #         carts.save()
        #     else:
        #         return CartResponse.failed("数据不存在", safe=False)

        # 采用 sku_id__in=sku_ids 批量修改
        update_count = models.Cart.objects.filter(email=email, sku_id__in=sku_ids, is_delete=0).update(is_delete=1)
        if update_count == 0:
            return CartResponse.failed("删除失败", safe=False)
        return CartResponse.success("删除成功", safe=False)


# class CartDetailAPIView(APIView):
#     def post(self, request):
#         if not request.user.get("status"):
#             return CartResponse.failed("登录状态已过期，请重新登录", safe=False)
#         email = request.user.get("payload").get("email")
#         filters = {
#             "email": email,
#             "is_delete": 0
#         }
#         shppiong_carts = models.Cart.objects.filter(**filters).all()
#         response_data = CartDetailSerializer(instance=shppiong_carts, many=True).data
#         return CartResponse.success(response_data)
class CartDetailAPIView(ListAPIView):
    queryset = models.Cart.objects
    serializer_class = CartDetailSerializer

    def post(self, request):
        if not request.user.get("status"):
            return CartResponse.failed("登录状态已过期，请重新登录", safe=False)
        email = request.user.get("payload").get("email")
        shppiong_carts = self.get_queryset().filter(email=email, is_delete=0).all()
        response_data = self.get_serializer(instance=shppiong_carts, many=True).data
        return CartResponse.success(response_data)


class UpdateCartNumberAPIView(APIView):
    def post(self, request):
        # 从 token 中获取数据
        if not request.user.get("status"):
            return CartResponse.failed("登录状态已过期，请重新登录", safe=False)
        email = request.user.get("payload").get("email")
        # post 请求中获取数据
        sku_id = request.data.get("sku_id")
        num = request.data.get("num")
        # 修改 购物车商品数量
        updated_count = models.Cart.objects.filter(email=email, sku_id=sku_id, is_delete=0).update(nums=num)
        if updated_count == 0:
            return CartResponse.failed("购物车记录不存在", safe=False)

        return CartResponse.success("修改成功")


# 获取购物车商品数量的接口
class CartCountAPIView(APIView):
    def get(self, request):
        # print(request.user)
        if not request.user.get("status"):
            return CartResponse.failed("登录状态已过期，请重新登录", safe=False)
        email = request.user.get("payload").get("email")

        # cart_count = models.Cart.objects.filter(email=email, is_delete=0).all().count()
        cart_count = models.Cart.objects.filter(email=email, is_delete=0).aggregate(Sum("nums"))
        # print(cart_count)
        return CartResponse.success(cart_count["nums__sum"] or 0)
