from django.db.models import Count
from rest_framework.views import APIView
from apps.classes.serializers import ClassListSerializer
from apps.classes.models import Class
from apps.user.models import User
from utils.ResponseMessage import check_auth, check_permission, MyResponse


class ClassOptionView(APIView):
    @check_permission
    def get(self, request):
        payload = request.user

        classes = Class.objects.all()
        if not classes:
            return MyResponse.failed("没有班级信息，请添加班级")
        response_data = []
        for c in classes:
            response_data.append({
                "id": c.id,
                "name": c.name,
                "grade": c.grade
            })

        print(response_data)
        return MyResponse.success(data=response_data)


class ClassListView(APIView):
    @check_permission
    def get(self, request):
        payload = request.user
        request_data = request.GET

        # name = 123 & grade = % E4 % B8 % 80 % E5 % B9 % B4 % E7 % BA % A7 & status = 1
        filter_body = {}
        page = int(request_data.get("page", 1))
        page_size = int(request_data.get("size", 10))
        for k, v in request_data.items():
            if k in ["page", "size"]:
                continue
            elif k == "name" and v:
                filter_body["name__icontains"] = v
            elif k in ["grade", "status"] and v:
                filter_body[k] = v

        offset = (page - 1) * page_size
        classes = Class.objects.filter(**filter_body).annotate(
            student_count=Count("userclass__user")
        )
        print(classes)
        if not classes:
            return MyResponse.failed(message="当前没有班级信息")

        response_data = {
            "list": [],
            "total": classes.count(),
            "page": page,
            "size": page_size
        }
        page_list = classes[offset:offset + page_size]
        try:
            for c in page_list:
                class_data = {}
                class_data["id"] = c.id
                class_data["name"] = c.name
                class_data["grade"] = c.grade
                class_data["head_teacher_id"] = c.head_teacher.id
                class_data["head_teacher_name"] = c.head_teacher.username
                class_data["student_count"] = c.student_count
                class_data["status"] = c.status
                class_data["create_time"] = c.create_time.strftime("%Y-%m-%d %H:%M:%S")
                response_data["list"].append(class_data)
            return MyResponse.success(data=response_data)
        except Exception as e:
            return MyResponse.failed(message=f"获取班级信息出错，{e}")


class ClassCreateView(APIView):
    @check_permission
    def post(self, request):
        payload = request.user

        request_data = request.data
        if not request_data.get("head_teacher_id"):
            return MyResponse.failed(message="请选择教师信息")

        try:
            user_teacher = User.objects.get(id=request_data["head_teacher_id"])
        except User.DoesNotExist:
            return MyResponse.failed(message="教师信息不存在")
        try:
            create_class = Class.objects.create(**request_data)

            return MyResponse.success(message="班级添加成功")
        except Exception as e:
            return MyResponse.failed(message=f"添加班级错误，{e}")



class ClassView(APIView):
    @check_permission
    def put(self, request, class_id):
        payload = request.user
        request_data = request.data
        if not request_data.get("head_teacher_id"):
            return MyResponse.failed(message="请选择教师信息")

        # 获取班级信息
        update_class = Class.objects.filter(id=class_id).update(**request_data)
        if not update_class:
            return MyResponse.failed(message="班级信息不存在")


        return MyResponse.success(message="修改班级信息成功")


