from django.shortcuts import render
from django.views import View
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.db.models import Q, F, QuerySet
from django.db.models import Model
from django.forms.models import model_to_dict
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

    def put(self, request: HttpRequest):
        """put 更新数据"""
        data = orjson.loads(request.body)
        print(data)

        # # 使用 save 更新数据
        # student = models.Student.objects.filter(name=data['name']).first()
        # if student:
        #     student.age = data['age']
        # student.save()
        # print(student.__dict__)

        # 使用 update 更新数据
        student = models.Student.objects.filter(name=data.get("name")).update(**data)
        print(student)

        return JsonResponse({}, status=200)

    def delete(self, request: HttpRequest):
        data = orjson.loads(request.body)
        # # 使用 delete() 删除
        # student = (models.Student.objects.filter(id=data.get("id")))
        # print(student)
        # if student:
        #     student.delete()
        # print(student)

        # 也可直接使用object.filter().delete()

        student = models.Student.objects.filter(name=data.get("name")).delete()
        print(student)  # 返回值为 # (1, {'student.Student': 1})

        return JsonResponse({}, status=200)


def queryset2dict(data, fields=None, exclude=None):
    """
    将QuerySet或模型实例转换为字典

    Args:
        data: QuerySet 或 模型实例
        fields: 指定要包含的字段列表
        exclude: 指定要排除的字段列表
    """
    result = {}
    if isinstance(data, QuerySet):
        result_list = []
        for item in data:
            if isinstance(item, Model):
                result_list.append(model_to_dict(item, fields=fields, exclude=exclude))
            elif isinstance(item, dict):
                result_list.append(item)
        result = {
            "count": len(data),
            "result": result_list,
        }
    elif isinstance(data, Model):
        result = {
            "count": 1,
            "result": model_to_dict(data),
        }
    elif isinstance(data, dict):
        result = {
            "count": 0,
            "result": data,
        }
    elif isinstance(data, list):
        result = {
            "count": len(data),
            "result": data,
        }
    return result


class StudentSearchView(View):
    def get(self, request: HttpRequest):
        students = {}
        # filter 过滤出符合条件的多个结果
        # exclude 排除掉符合条件的多个结果，与filter相反，与filter互斥。
        # get 过滤单一结果, 结果不是一个，会报错。

        # # exact 过滤相等的条件
        # students = models.Student.objects.filter(name="吴杰").all()  # 简写方式，这个最常用！！
        # print(students, type(students))

        # # contains：是否包含
        # # name__contains -> 包含 ---> name like "%王%"
        # students = models.Student.objects.filter(name__contains="王")
        # print(students, type(students))

        # # startswith、endswith：以指定值开头或结尾。
        # # name__startswith ---> name like "华%"
        # students = models.Student.objects.filter(name__startswith="张")
        # print(students, type(students))
        # # name__endswith ---> name like "%华"
        # students = models.Student.objects.filter(name__endswith="华")
        # print(students, type(students))

        # # isnull：字段值是否为null。
        # # 查询数据为null
        # students = models.Student.objects.filter(description__isnull=True)

        # # in ：是否包含在范围内。
        # students = models.Student.objects.filter(classmate__in=["304", "305", "306"]).values("id", "name", "classmate")
        # print(students, type(students[0]))

        # #  range : 取值范围
        # # SQL: SELECT ... WHERE id BETWEEN 51 and 67;
        # students = models.Student.objects.filter(id__range=(1, 30)).values("id", "name")

        #  比较查询
        # gt 大于 (greater then)
        # gte 大于等于 (greater then equal)
        # lt 小于 (less then)
        # lte 小于等于 (less then equal)

        # # SQL: select * from student where age > 22;
        # students = models.Student.objects.filter(age__gt=22)

        # # SQL: select * from student where id <= 50 and id >= 20;
        # students = models.Student.objects.filter(id__gte=20, id__lte=50)

        # # 年龄不等于19的
        # # 使用exclude把符合条件的排除掉 , 不等于的运算符，使用exclude()过滤器。
        # students = models.Student.objects.exclude(age=19)

        # 日期查询
        # 注意
        # django的ORM中提供了许多方法用于进行日期的查询过滤，
        # 例如：year、month、day、week_day、hour、minute、second都可以对日期时间类型的属性进行运算。
        # 要进行日期时间的过滤查询，必须保证python代码中使用的时间时区与mysql数据库中的时间时区是对应的！
        # 如果mysql的时区与python代码的时区不对应，则得到的结果纯在时区的差异。
        # 需要调整settings.py的时区配置项为：USE_TZ = False

        # 查询2017年被加入数据表的信息
        # created_time__year=2017  ---> where year(created_time)=2017
        # students = models.Student.objects.filter(created_time__year=2025)

        # 查询11月份被加入数据表的信息
        # SQL: where month(created_time) = 11;
        # students = models.Student.objects.filter(created_time__month=11)

        # # 查询出2022年07月份的学生
        # # SQL: WHERE month(created_time) = 7 AND year(created_time) = 2022;
        # students = models.Student.objects.filter(created_time__year=2022, created_time__month=7).values("name", "created_time")

        # # 查询出2017年11月20号的学生
        # # SQL: WHERE month(created_time) = 7 AND year(created_time) = 2022 AND day(created_time);
        # students = models.Student.objects.filter(
        #     created_time__year=2017,
        #     created_time__month=7,
        #     created_time__day=20
        # ).values("name", "created_time")

        # # 查询7月20号的学生
        # # SQL: where month(created_time) = 7 and day(created_time) = 20
        # students = models.Student.objects.filter(created_time__month=7, created_time__day=20)

        # """精确时间查询"""
        # # 方式1：当在模型使用datetime指定字段的数据类型以后，就不能直接通过字符串的比较来过滤查询了，
        # # 因为字符串时间格式无法与datetime对象来进行很精确的判断比较
        # students = models.Student.objects.filter(created_time="2021-08-18 16:19:38").all()
        # print(student_objs)

        # # 方式2：把字符窜格式的时间转换成datetime对象，也可以查询。
        # from django.utils.timezone import datetime
        # # 把字符串格式时间转换成datetime时间戳对象
        # timestamp = datetime.strptime("2021-08-18 16:19:38", "%Y-%m-%d %H:%M:%S")
        # students = models.Student.objects.filter(created_time=timestamp).all()
        # print(student_objs)

        # """判断两个时间范围"""
        # time1 = "2020-11-20 9:00:00"
        # time2 = "2020-11-20 11:00:00"
        # # 查询添加时间在time1与time2之间的学生信息
        # students = models.Student.objects.filter(
        #     created_time__gte=time1,
        #     created_time__lte=time2,
        # ).all()

        """
        # F对象
        # F对象，主要用于在SQL语句中针对字段之间的值进行比较的查询。
        # 之前的查询都是对象的属性与常量值比较，两个属性怎么比较呢？ 答：使用F对象，被定义在django.db.models中。
        """

        # # 查询出入学以后，数据没有被修改过的学生信息
        # students = models.Student.objects.filter(created_time=F("created_time"))

        """
         Q对象
         多个过滤器逐个调用表示逻辑与关系，同sql语句中where部分的and关键字。
         如果需要实现逻辑或or的查询，需要使用Q()对象结合|运算符
        """
        # # 304 班级的，女同学
        # students = models.Student.objects.filter(Q(sex=False) & Q(classmate=304))

        # # 查询 name，或 mobile 是否存在
        # students = models.Student.objects.filter(Q(name="李亚容") | Q(mobile="13312345640"))

        # # 多个或，or Q(条件) | Q(条件)
        # # 查询出301班的男生 或者 302班的男生
        # students = models.Student.objects.filter(Q(classmate=301, sex=True) | Q(classmate=302, sex=True))

        # # 上面完全可以简写成
        # students = models.Student.objects.filter(classmate__in=[301, 302], sex=True)

        # # 如果是这样则不能简写了
        # # 查询出301班年龄大于21男生，或者 302班年龄小于19岁的女生
        # students = models.Student.objects.filter(
        #     Q(classmate=301, sex=True, age__gt=21) | Q(classmate=302, age__lt=19, sex=False)
        # )

        # Q对象可以使用& 表示逻辑与（and），| 表示逻辑或（or），~表示逻辑非（not）
        # 年龄不等于19的, 可以将 exclude, 用 ~Q 替换
        students = models.Student.objects.filter(~Q(age=19))

        return JsonResponse({"data": queryset2dict(students)}, status=200)
