from rest_framework.views import APIView
from django.db.models import Count, Q
from apps.user.models import User
from apps.exam.models import Exam, ExamRecord
from apps.question.models import Question
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
        payload = request.user
        
        users = User.objects.all()
        total_users = users.count()
        response_data = {
            "total_users": total_users,
            "student_count": 0,
            "teacher_count": 0,
            "admin_count": 0,
            "active_users": 0,
            "disabled_users": 0,
        }
        
        for user in users:
            if user.role == "student":
                response_data["student_count"] += 1
            elif user.role == "teacher":
                response_data["teacher_count"] += 1
            elif user.role == "admin":
                response_data["admin_count"] += 1
            elif user.status == 1:
                response_data["active_users"] += 1
            elif user.status == 0:
                response_data["disabled_users"] += 1
        
        return MyResponse.success(data=response_data)
    

class UserInfoView(APIView):
    @check_permission
    def get(self, request, user_id):
        payload = request.user
        
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return MyResponse.failed(message="用户信息不存在")
        
        ser_user_data = UserSerializers(instance=user).data
        # print(ser_user_data)
        try:
            exam_count = Exam.objects.filter(creator_id=user_id).count()
            question_count = Question.objects.filter(creator_id=user_id).count()
            record_count = ExamRecord.objects.filter(user_id=user_id).count()

            ser_user_data["exam_count"] = exam_count
            ser_user_data["question_count"] = question_count
            ser_user_data["record_count"] = record_count
            
            return MyResponse.success(data=ser_user_data)
        except Exception as e:
            return MyResponse.failed(f"获取数据出错，{e}")
        
        
class UserUpdateStatusView(APIView):
    @check_permission
    def put(self, request, user_id):
        payload = request.user
        
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return MyResponse.failed(message="用户信息不存在")
        
        
        status = request.data.get("status", 0)
        
        update_count = User.objects.filter(id=user_id).update(status=status)
        if not update_count:
            return MyResponse.failed(message="修改状态失败")
        return MyResponse.success("修改成功")