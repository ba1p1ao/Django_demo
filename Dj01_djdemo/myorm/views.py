from django.shortcuts import render
from django.views import View
from django.http import HttpResponse, HttpRequest
from myorm import models


# Create your views here.
class StudentView(View):
    """1：1模型关联"""

    # def getCreateData(self, request):
    #     # # 添加数据
    #     # # 先添加 主模型数据students， 再添加外键模型数据studentprofile
    #
    #     # student = models.Student.objects.create(
    #     #     name="小红",
    #     #     age="20",
    #     #     sex="1",
    #     # )
    #     # profile = models.StudentProfile.objects.create(
    #     #     student_id=student.id, # 等价于下面
    #     #     # student=student,
    #     #     description="一段长长长长的个性签名....",
    #     #     address="学生小红的家庭住址",
    #     #     mobile="13312345668",
    #     # )
    #
    #     # 方式二
    #     # profile = models.StudentProfile.objects.create(
    #     #     student=models.Student.objects.create(
    #     #         name="小灰",
    #     #         age="21",
    #     #         sex="0",
    #     #     ),
    #     #     description="一段长长长长的个性签名....",
    #     #     address="学生小灰的家庭住址",
    #     #     mobile="13312345468",
    #     # )
    #
    #     return HttpResponse("hello")


    # def getSearch(self, request: HttpRequest):
    #     """查询数据"""
    #     # # 从主模型 (主表，orm_student) 查询到外键模型 (附加表，orm_student_profile)
    #     # # 方式1:
    #     # # 例如，李华今天没上学，查询他的紧急联系电话和家庭地址
    #     # student = models.Student.objects.get(name="李华")
    #     # print(student) # {'id': 1, 'name': '李华', 'age': 20}
    #     # print(student.profile) # {'address': '学生李华的家庭住址', 'mobile': '13312345668'}
    #
    #     # # 方式2：直接使用外键模型，通过主键参数查询
    #     # # 例如，李华今天没上学，查询他的紧急联系电话和家庭地址
    #     # student = models.StudentProfile.objects.get(student__name="李华")
    #     # print(student) # {'address': '学生李华的家庭住址', 'mobile': '13312345668'}
    #
    #
    #     # ## 从外键模型查询到主键模型数据
    #     # # 方式1
    #     # # 例如：查询手机号为：13312345662 的学生信息
    #     # student_profile = models.StudentProfile.objects.get(mobile="13312345662")
    #     # print(student_profile) # {'address': '学生小红的家庭住址', 'mobile': '13312345662'}
    #     # print(student_profile.student) # {'id': 2, 'name': '小红', 'age': 20}
    #
    #     # # 方式2
    #     # # 例如：查询手机号为：13312345662 的学生信息
    #     # student = models.Student.objects.get(profile__mobile="13312345662")
    #     # print(student) # {'id': 2, 'name': '小红', 'age': 20}
    #
    #
    #
    #     return HttpResponse("ok")

    def get(self, request: HttpRequest):
        """删除操作"""
        # # on delete=models.CASCADE 表示删除主模型数据时，对应的外键模型数据也会被删除
        # student = models.Student.objects.filter(id=1).delete()
        # print(student) # (2, {'myorm.StudentProfile': 1, 'myorm.Student': 1})

        # # on delete=models.CASCADE 删除外键型数据时， 不会影响主键模型的数据
        # student = models.StudentProfile.objects.filter(student__name="小红").delete()
        # print(student) # (1, {'myorm.StudentProfile': 1})


        return HttpResponse("ok")

