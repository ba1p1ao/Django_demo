"""
0 : 数据返回成功
1 : 数据返回失败
2 : 数据返回出现异常
"""

from django.http import JsonResponse


# 菜单响应类： 1XXXX
class MenuResponse:
    @staticmethod
    def success(data, safe=True):
        response_data = {"status": 10000, "data": data}
        return JsonResponse(response_data, safe=safe)

    @staticmethod
    def failed(data, safe=True):
        response_data = {"status": 10001, "data": data}
        return JsonResponse(response_data, safe=safe)

    @staticmethod
    def other(data, safe=True):
        response_data = {"status": 10002, "data": data}
        return JsonResponse(response_data, safe=safe)


# 商品响应类： 2XXXX
class GoodsResponse:
    @staticmethod
    def success(data, safe=True):
        response_data = {"status": 20000, "data": data}
        return JsonResponse(response_data, safe=safe)

    @staticmethod
    def failed(data, safe=True):
        response_data = {"status": 20001, "data": data}
        return JsonResponse(response_data, safe=safe)

    @staticmethod
    def other(data, safe=True):
        response_data = {"status": 20002, "data": data}
        return JsonResponse(response_data, safe=safe)


# 购物车响应类： 3XXXX
class CartResponse:
    @staticmethod
    def success(data, safe=True):
        response_data = {"status": 30000, "data": data}
        return JsonResponse(response_data, safe=safe)

    @staticmethod
    def failed(data, safe=True):
        response_data = {"status": 30001, "data": data}
        return JsonResponse(response_data, safe=safe)

    @staticmethod
    def other(data, safe=True):
        response_data = {"status": 30002, "data": data}
        return JsonResponse(response_data, safe=safe)



# 用户响应类： 4XXXX
class UserResponse:
    @staticmethod
    def success(data, safe=True):
        response_data = {"status": 40000, "data": data}
        return JsonResponse(response_data, safe=safe)

    @staticmethod
    def failed(data, safe=True):
        response_data = {"status": 40001, "data": data}
        return JsonResponse(response_data, safe=safe)

    @staticmethod
    def other(data, safe=True):
        response_data = {"status": 40002, "data": data}
        return JsonResponse(response_data, safe=safe)

# 评论响应类： 5XXXX
class CommentResponse:
    @staticmethod
    def success(data, safe=True):
        response_data = {"status": 50000, "data": data}
        return JsonResponse(response_data, safe=safe)

    @staticmethod
    def failed(data, safe=True):
        response_data = {"status": 50001, "data": data}
        return JsonResponse(response_data, safe=safe)

    @staticmethod
    def other(data, safe=True):
        response_data = {"status": 50002, "data": data}
        return JsonResponse(response_data, safe=safe)


# 订单响应类： 6XXXX
class OrderResponse:
    @staticmethod
    def success(data, safe=True):
        response_data = {"status": 60000, "data": data}
        return JsonResponse(response_data, safe=safe)

    @staticmethod
    def failed(data, safe=True):
        response_data = {"status": 60001, "data": data}
        return JsonResponse(response_data, safe=safe)

    @staticmethod
    def other(data, safe=True):
        response_data = {"status": 60002, "data": data}
        return JsonResponse(response_data, safe=safe)


# 用户地址响应类： 7XXXX
class AddressResponse:
    @staticmethod
    def success(data, safe=True):
        response_data = {"status": 70000, "data": data}
        return JsonResponse(response_data, safe=safe)

    @staticmethod
    def failed(data, safe=True):
        response_data = {"status": 70001, "data": data}
        return JsonResponse(response_data, safe=safe)

    @staticmethod
    def other(data, safe=True):
        response_data = {"status": 70002, "data": data}
        return JsonResponse(response_data, safe=safe)


# 用户地址响应类： 8XXXX
class PayResponse:
    @staticmethod
    def success(data, safe=True):
        response_data = {"status": 80000, "data": data}
        return JsonResponse(response_data, safe=safe)

    @staticmethod
    def failed(data, safe=True):
        response_data = {"status": 80001, "data": data}
        return JsonResponse(response_data, safe=safe)

    @staticmethod
    def other(data, safe=True):
        response_data = {"status": 80002, "data": data}
        return JsonResponse(response_data, safe=safe)


# 工具响应类： 9XXXX
class ToolsResponse:
    @staticmethod
    def success(data, safe=True):
        response_data = {"status": 90000, "data": data}
        return JsonResponse(response_data, safe=safe)

    @staticmethod
    def failed(data, safe=True):
        response_data = {"status": 90001, "data": data}
        return JsonResponse(response_data, safe=safe)

    @staticmethod
    def other(data, safe=True):
        response_data = {"status": 90002, "data": data}
        return JsonResponse(response_data, safe=safe)