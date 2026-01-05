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
        | class_id | int | 否 | 班级ID |
        """
        from apps.classes.models import UserClass, Class

        payload = request.user
        request_data = request.GET
        # 设置过滤参数
        filter_body = {}
        class_id = None
        for k, v in request_data.items():
            if k in ["page", "size"]:
                continue
            elif k == "class_id" and v:
                class_id = int(v)
            elif k in ["role", "status"] and v:
                filter_body[f"{k}"] = v
            elif k in ["username", "nickname"] and v:
                filter_body[f"{k}__icontains"] = v

        page = int(request_data.get("page", 1))
        page_size = int(request_data.get("size", 10))
        offset = (page - 1) * page_size

        users = User.objects.filter(**filter_body)

        # 如果有班级筛选，需要通过 UserClass 表来筛选
        if class_id:
            user_ids = UserClass.objects.filter(class_info_id=class_id).values_list('user_id', flat=True)
            users = users.filter(id__in=user_ids)

        total = users.count()
        page_list = users.order_by("-create_time")[offset:offset+page_size]

        if not page_list:
            response_data = {
                "list": [],
                "total": 0,
                "page": page,
                "size": page_size,
            }
            return MyResponse.success(data=response_data)

        total = users.count()
        page_list = users.order_by("-create_time")[offset:offset+page_size]

        ser_data = UserSerializers(instance=page_list, many=True).data

        # 为每个用户添加班级信息
        for user_data in ser_data:
            user_id = user_data["id"]
            try:
                # 获取用户的班级信息
                user_class = UserClass.objects.filter(user_id=user_id).select_related('class_info').first()
                if user_class and user_class.class_info:
                    user_data["class_name"] = user_class.class_info.name
                    user_data["class_id"] = user_class.class_info.id
                else:
                    user_data["class_name"] = None
                    user_data["class_id"] = None
            except Exception as e:
                user_data["class_name"] = None
                user_data["class_id"] = None

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
    
    
    @check_permission
    def delete(self, request, user_id):
        payload = request.user
        
        if user_id == payload.get("id"):
            return MyResponse.failed(message="不能删除自己")

        delete_count = User.objects.filter(id=user_id).delete()
        if not delete_count:
            return MyResponse.failed("用户删除失败")
        return MyResponse.success("用户删除成功")
        
        
class UserUpdateStatusView(APIView):
    @check_permission
    def put(self, request, user_id):
        payload = request.user
        if user_id == payload.get("id"):
            return MyResponse.failed(message="当前状态下不能修改自己的状态")
        
        status = request.data.get("status", 0)
        
        update_count = User.objects.filter(id=user_id).update(status=status)
        if not update_count:
            return MyResponse.failed(message="修改用户状态失败")
        return MyResponse.success("修改用户状态成功")


class UserUpdateRoleView(APIView):
    @check_permission
    def put(self, request, user_id):
        payload = request.user
        if user_id == payload.get("id"):
            return MyResponse.failed(message="当前状态下不能修改自己的角色")
    
        role = request.data.get("role", 0)
        
        update_count = User.objects.filter(id=user_id).update(role=role)
        if not update_count:
            return MyResponse.failed(message="修改用户角色失败")
        return MyResponse.success("修改用户角色成功")
    
    
    