from django.db.models import Count, F, Q, Avg, Max, Min, Case, When, FloatField
from rest_framework.views import APIView
from apps.classes.serializers import ClassListSerializer
from apps.classes.models import Class, UserClass
from apps.exam.models import ExamRecord
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

        return MyResponse.success(message="修改成功")

    @check_permission
    def delete(self, request, class_id):
        payload = request.user
        try:
            # 检查班级是否存在
            class_obj = Class.objects.get(id=class_id)
            # 删除班级，由于 UserClass 的 on_delete=CASCADE，会自动删除关联的学生班级记录
            class_obj.delete()

            return MyResponse.success(message="删除成功")
        except Class.DoesNotExist:
            return MyResponse.failed(message="班级信息不存在")
        except Exception as e:
            return MyResponse.failed(message=f"删除失败: {str(e)}")


class ClassStatusView(APIView):
    @check_permission
    def put(self, request, class_id):
        payload = request.user

        # 获取班级信息
        try:
            class_obj = Class.objects.get(id=class_id)
            new_status = 0 if class_obj.status == 1 else 1
            update_class = Class.objects.filter(id=class_id).update(status=new_status)
            if update_class == 0:
                return MyResponse.failed(message="班级信息不存在")

            return MyResponse.success(message="修改成功")
        except Class.DoesNotExist:
            return MyResponse.failed(message="班级信息不存在")


class ClassStatisticsView(APIView):
    @check_permission
    def get(self, request, class_id):
        payload = request.user

        try:
            class_obj = Class.objects.get(id=class_id)
        except Class.DoesNotExist:
            return MyResponse.failed(message="班级信息不存在")

        response_data = {
            "class_id": class_obj.id,
            "class_name": class_obj.name,
            "student_count": 0,
            "exam_count": 0,
            "average_score": 0.00,
            "highest_score": 0.00,
            "lowest_score": 0.00,
            "pass_rate": 0.00,
            "excellent_rate": 0.00,
            "score_distribution": {
                "0-59": 0,
                "60-69": 0,
                "70-79": 0,
                "80-89": 0,
                "90-100": 0
            }
        }

        student_class_qs = UserClass.objects.filter(class_info=class_id)
        response_data["student_count"] = student_class_qs.count()

        if response_data["student_count"] == 0:
            return MyResponse.success(data=response_data)

        student_ids = [s.user_id for s in student_class_qs]

        graded_records = ExamRecord.objects.filter(user_id__in=student_ids, status="graded")
        response_data["exam_count"] = graded_records.count()

        if response_data["exam_count"] == 0:
            return MyResponse.success(data=response_data)

        class_exam_score = graded_records.aggregate(
            average_score=Avg("score"),
            highest_score=Max("score"),
            lowest_score=Min("score"),
            pass_rate=Avg(
                Case(
                    When(is_passed=1, then=1.0),
                    When(is_passed=0, then=0.0),
                    default=None,
                    output_field=FloatField()
                )
            ),
            excellent_rate=Avg(
                Case(
                    When(score__gte=80, then=1.0),
                    When(score__lt=80, then=0.0),
                    default=None,
                    output_field=FloatField()
                )
            )
        )

        response_data["average_score"] = round(class_exam_score["average_score"] or 0, 2)
        response_data["highest_score"] = round(class_exam_score["highest_score"] or 0, 2)
        response_data["lowest_score"] = round(class_exam_score["lowest_score"] or 0, 2)
        response_data["pass_rate"] = round(class_exam_score["pass_rate"] or 0, 2)
        response_data["excellent_rate"] = round(class_exam_score["excellent_rate"] or 0, 2)

        student_max_scores = graded_records.values("user_id").annotate(max_score=Max("score"))
        for er in student_max_scores:
            max_score = er["max_score"]
            if max_score >= 90:
                response_data["score_distribution"]["90-100"] += 1
            elif max_score >= 80:
                response_data["score_distribution"]["80-89"] += 1
            elif max_score >= 70:
                response_data["score_distribution"]["70-79"] += 1
            elif max_score >= 60:
                response_data["score_distribution"]["60-69"] += 1
            else:
                response_data["score_distribution"]["0-59"] += 1

        return MyResponse.success(data=response_data)


class ClassMembersView(APIView):
    @check_permission
    def get(self, request, class_id):
        payload = request.user

        try:
            class_obj = Class.objects.get(id=class_id)
        except Class.DoesNotExist:
            return MyResponse.failed(message="班级信息不存在")

        page = int(request.GET.get("page", 1))
        page_size = int(request.GET.get("size", 10))
        offset = (page - 1) * page_size

        role = request.GET.get("role", "")

        user_class_qs = UserClass.objects.filter(class_info=class_id)

        if role:
            user_class_qs = user_class_qs.filter(user__role=role)

        total = user_class_qs.count()

        response_data = {
            "class_id": class_obj.id,
            "class_name": class_obj.name,
            "list": [],
            "total": total,
            "page": page,
            "size": page_size,
        }

        if total == 0:
            return MyResponse.success(data=response_data)

        student_list = user_class_qs.select_related('user')[offset:offset + page_size]

        for student in student_list:
            data = {
                "id": student.user.id,
                "username": student.user.username,
                "nickname": student.user.nickname,
                "role": student.user.role,
                "avatar": student.user.avatar,
                "status": student.user.status,
                "join_time": student.join_time.strftime("%Y-%m-%d %H:%M:%S"),
            }
            response_data["list"].append(data)

        return MyResponse.success(data=response_data)