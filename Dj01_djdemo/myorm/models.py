from django.db import models
from django.db.models import DO_NOTHING

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

    student = models.OneToOneField(to="Student", related_name="profile", on_delete=models.CASCADE, verbose_name="学生")
    description = models.TextField(default="", verbose_name="个性签名")
    address = models.CharField(max_length=500, verbose_name="家庭住址")
    mobile = models.CharField(max_length=15, verbose_name="紧急联系电话")

    class Meta:
        db_table = "orm_student_profile"
        verbose_name = db_table
        verbose_name_plural = verbose_name

    def __str__(self):
        return str({"address": self.address, "mobile": self.mobile})


"""
一对多
"""


class Auther(models.Model):
    name = models.CharField(max_length=50, verbose_name="姓名")
    age = models.IntegerField(verbose_name="年龄")
    sex = models.BooleanField(null=True, blank=True, default=None, verbose_name="性别")

    class Meta:
        db_table = 'orm_auther'
        verbose_name = db_table
        verbose_name_plural = verbose_name

    def __str__(self):
        return str({"name": self.name, "age": self.age, "sex": self.sex})


class Article(models.Model):
    # DO_NOTHING 不能实现，删除外键关联的主键
    # 需要添加 on_delete=models.SET_NULL, null=True 才能实现删除主键，外键的值这是为空
    # auther = models.ForeignKey(to="Auther", on_delete=models.DO_NOTHING, related_name="article", verbose_name="作者")
    auther = models.ForeignKey(to="Auther", on_delete=models.SET_NULL, null=True, related_name="article", verbose_name="作者")
    title = models.CharField(max_length=50, verbose_name="文章标题")
    content = models.TextField(null=True, verbose_name="文章内容")
    pubdate = models.DateTimeField(null=True, verbose_name="发布时间")
    created_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    updated_time = models.DateTimeField(auto_now=True, verbose_name="创建时间")

    class Meta:
        db_table = "orm_article"
        verbose_name = db_table
        verbose_name_plural = verbose_name

    def __str__(self):
        return str({"title": self.title, "content": self.content, "pubdate": self.pubdate})



"""
多对多
"""


class Teacher(models.Model):
    name = models.CharField(max_length=50, verbose_name="姓名")
    age = models.IntegerField(verbose_name="年龄")
    sex = models.BooleanField(null=True, blank=True, default=None, verbose_name="性别")

    # Course 中的外键一下面的外键一样，因为是多对多字段，可以写在 Teacher 中，也可以写在 Course 中，
    # 但是一定区分好， to 与 related_name 的值
    # 在 Teacher中， to="Course", related_name="teacher"
    # 在 Course 中， to="Teacher", related_name="course"
    # course = models.ManyToManyField("Course", related_name="teacher", verbose_name="课程信息")
    # django 会自动创建一个关系表 orm_teacher_course
    class Meta:
        db_table = 'orm_teacher'
        verbose_name = db_table
        verbose_name_plural = verbose_name

    def __str__(self):
        return str({"name": self.name, "age": self.age, "sex": self.sex})


class Course(models.Model):
    name = models.CharField(max_length=50, verbose_name="课程名")
    teacher = models.ManyToManyField("Teacher", related_name="course", verbose_name="教师信息")
    # django 会自动创建一个关系表 orm_course_teacher
    class Meta:
        db_table = 'orm_course'
        verbose_name = db_table
        verbose_name_plural = verbose_name

    def __str__(self):
        return str({"name": self.name})