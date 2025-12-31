from rest_framework.views import APIView

from apps.user.models import User
from apps.user.serializers import UserSerializers
from utils.ResponseMessage import check_permission, check_auth, MyResponse


class UserListView(APIView):
    @check_permission
    def get(self, request):
        """
        | 参数名 | 类型 | 必填 | 说明 |
        |--------|------|------|------|
        | page | int | 否 | 页码，默认1 |
        | size | int | 否 | 每页数量，默认10 |
        | username | string | 否 | 用户名（模糊搜索） |
        | nickname | string | 否 | 昵称（模糊搜索） |
        | role | string | 否 | 角色：student/teacher/admin |
        | status | int | 否 | 状态：1正常 0禁用 |
        """
        payload = request.user
        request_data = request.GET
        # 设置过滤参数
        filter_body = {}
        for k, v in request_data.items():
            if k in ["page", "size"]:
                continue
            elif k in ["role", "status"] and v:
                filter_body[f"{k}"] = v
            elif k in ["username", "nickname"] and v:
                filter_body[f"{k}__icontains"] = v
        
        page = int(request_data.get("page", 1))
        page_size = int(request_data.get("size", 10))
        offset = (page - 1) * page_size
        
        users = User.objects.filter(**filter_body)
        
        if not users:
            return MyResponse.failed(message="用户信息为空")     
        total = users.count()
        page_list = users.order_by("-create_time")[offset:offset+page_size]
        
        ser_data = UserSerializers(instance=page_list, many=True).data
        response_data = {
            "list": ser_data,
            "total": total,
            "page": page,
            "size": page_size,
        }
        
        return MyResponse.success(data=response_data)

class UserStatisticsView(APIView):
    @check_permission
    def get(self, request):
        return MyResponse.failed()