from django.db import models

# Create your models here.
"""
1.django中所有的模型，必须直接或间接继承models.Model模型基类
"""
from datetime import datetime


class BaseModel(models.Model):
    # auto_now_add 设置新建数据时，把当前时间戳作为默认值保存到当前字段中
    created_time = models.DateTimeField(auto_now_add=True, null=True, verbose_name="创建时间")
    # auto_now 设置修改数据时，把当前时间戳作为默认值保存到当前字段中
    updated_time = models.DateTimeField(auto_now=True, null=True, verbose_name="修改时间")

    class Meta:
        # 设置当前类为抽象模型，表示当前模型并不是一个真正的表，django就不会跟踪识别这个模型了。
        abstract = True


# 继承公共类
class Student(BaseModel):
    STATUS = (
        # (数据库值, "程序显示给外界看的文本"),
        (0, "未毕业"),
        (1, "未入学"),
        (2, "已毕业"),
    )
    id = models.IntegerField(primary_key=True, verbose_name="id")
    name = models.CharField(max_length=255, db_index=True, unique=True, verbose_name="姓名")
    classmate = models.CharField(max_length=50, db_column="class", db_index=True, default="", verbose_name="班级编号")
    age = models.IntegerField(verbose_name="年龄")
    sex = models.BooleanField(default=True, verbose_name="性别")
    mobile = models.CharField(max_length=50, db_index=True, unique=True, verbose_name="手机号")
    status = models.IntegerField(default=0, choices=STATUS, verbose_name="毕业状态")
    description = models.TextField(blank=True, null=True, verbose_name="个性签名")

    class Meta:
        db_table = "student"
        verbose_name = "学生信息"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name
