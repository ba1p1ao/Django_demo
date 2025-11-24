from django.db import models

# Create your models here.
"""
一对一模型关联
"""


class Student(models.Model):
    # 默认添加 id
    name = models.CharField(max_length=20, db_index=True, verbose_name="姓名")
    age = models.IntegerField(verbose_name="年龄")
    sex = models.BooleanField(null=True, blank=True, default=None, verbose_name="性别")
    created_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    updated_time = models.DateTimeField(auto_now=True, verbose_name="更新时间")

    class Meta:
        db_table = "orm_student"
        verbose_name = db_table
        verbose_name_plural = verbose_name

    def __str__(self):
        return str({"id": self.id, "name": self.name, "age": self.age})


class StudentProfile(models.Model):
    # on_delete
    # CASCADE：级联删除。删除父表记录时，同时删除所有关联的子表记录。
    # PROTECT：保护。如果子表有记录关联父表，则禁止删除父表记录。
    # SET_NULL：将子表中的外键字段设置为 NULL。
    # SET_DEFAULT：将子表中的外键字段设置为默认值。
    # DO_NOTHING：不执行任何操作，子表记录仍然指向已被删除的父表记录。

    student = models.OneToOneField("Student", related_name="profile", on_delete=models.CASCADE, verbose_name="学生")
    description = models.TextField(default="", verbose_name="个性签名")
    address = models.CharField(max_length=500, verbose_name="家庭住址")
    mobile = models.CharField(max_length=15, verbose_name="紧急联系电话")

    class Meta:
        db_table = "orm_student_profile"
        verbose_name = db_table
        verbose_name_plural = verbose_name

    def __str__(self):
        return str({"address": self.address, "mobile": self.mobile})

