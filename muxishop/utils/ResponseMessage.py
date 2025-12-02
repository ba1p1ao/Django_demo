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
