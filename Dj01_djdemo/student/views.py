from django.shortcuts import render
from django.views import View
from django.http import HttpRequest, HttpResponse, JsonResponse
from student import models
import json
# Create your views here.
class StudentView(View):
    def get(self, request: HttpRequest):
        """获取学生信息"""
        student_list = []
        objects = models.Student.objects.all()
        students = models.Student.objects.filter(age__gt=20).values()
        students = list(students)
        # student_dict = dict(students)
        table_header = []
        student = students[0]
        print(student.get("name"))
        table_header = student.keys()
        print(student, table_header)
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
        return render(request, "student_list.html", locals())
        return HttpResponse(student)