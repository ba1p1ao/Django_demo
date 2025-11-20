from django.shortcuts import render
from django.views import View
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.db.models import Q
from student import models
import orjson
# Create your views here.
class StudentView(View):
    def get(self, request: HttpRequest):
        """获取学生信息"""

        """使用 get"""
        # # get 获取符合查询条件的一条数据，如果获取不到则抛出 DoesNotExists 异常，
        # # 如果获取到符合条件的数据有多条也会报错。抛出 MultipleObjectsReturned 异常，
        # # 如果查询条件不匹配，抛出异常
        #
        # # get 在实际开发中，更多使用用于给开发者基于ID主键 / 唯一索引来获取一条数据
        #
        # try:
        #     name = request.GET.get("name")
        #     # student = models.Student.objects.get(name=name)
        #     student = models.Student.objects.get(id=12)
        #     result = {
        #         "code": 1,
        #         "msg": "查询成功",
        #         "data": {
        #             "name": student.name,
        #             "classmate": student.classmate,
        #             "age": student.age,
        #             "sex": student.sex,
        #         },
        #     }
        # except Exception:
        #     result = {
        #         "code": -1,
        #         "msg": "用户名错误",
        #         "data": {},
        #     }
        # # filter 条件过滤
        # print(result)
        # return JsonResponse(result)


        """使用 first"""
        # student = models.Student.objects.all().first()
        # print(student) # 赵华

        # student = models.Student.objects.filter(classmate=304).first()
        # print(student)

        # 如果查询的数据不存在，返回None
        # student = models.Student.objects.filter(name="asdf").first()
        # print(student) # None

        """使用filter"""

        # students = models.Student.objects.filter(classmate="304")
        # print(students) # <QuerySet [<Student: 江俊文>, <Student: 李亚容>]>

        """使用count"""

        student_count = models.Student.objects.filter(sex=True).count()
        print(student_count)

        return JsonResponse({}, safe=True)
        # students = models.Student.objects.filter(age__gt=20).values()
        # students = list(students)
        # # student_dict = dict(students)
        # table_header = []
        # student = students[0]
        # print(student.get("name"))
        # table_header = student.keys()
        # print(student, table_header)
        # student_list = []
        # for object in objects:
        #     student_list.append({
        #         "name": object.name,
        #         "class": object.classmate,
        #         "age": object.age,
        #     })
        #     print(object.name)
        # print(student_list)
        # print(students, type(students))
        # return render(request, "student_list.html", locals())
        # return HttpResponse(student)

    def post(self, request: HttpRequest):
        """post 请求添加数据"""
        # form 表单数据 request.body 识别不了，只能采用request.POST
        data = orjson.loads(request.body)

        student = models.Student.objects.filter(Q(name=data.get("name")) | Q(mobile=data.get("mobile")))
        if student:
            return HttpResponse("用户或手机号已存在", status=403)

        print(data)

        # 使用 save 添加数据
        # student = models.Student(**data)
        # student.save() # 添加到数据库

        # 使用 create 添加数据
        student = models.Student.objects.create(**data)


        print(student.id, student.name)

        return JsonResponse(data, status=200, safe=False)

