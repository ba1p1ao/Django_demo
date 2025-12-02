"""
0 : 数据返回成功
1 : 数据返回失败
2 : 数据返回出现异常
"""

from django.http import JsonResponse


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
