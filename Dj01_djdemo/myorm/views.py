from wsgiref.util import application_uri

from django.shortcuts import render
from django.views import View
from django.http import HttpResponse, HttpRequest, JsonResponse
from myorm import models

"""
开启数据库查询日志

show variables like "%general_log%";

+------------------+---------------------------------+
| Variable_name    | Value                           |
+------------------+---------------------------------+
| general_log      | OFF                             |
| general_log_file | /var/lib/mysql/ff969a281c3a.log |
+------------------+---------------------------------+

set global general_log = 'ON'; 
tail -f /var/lib/mysql/ff969a281c3a.log

"""


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

    # def get(self, request: HttpRequest):
    #     """删除操作"""
    #     # # on delete=models.CASCADE 表示删除主模型数据时，对应的外键模型数据也会被删除
    #     # student = models.Student.objects.filter(id=1).delete()
    #     # print(student) # (2, {'myorm.StudentProfile': 1, 'myorm.Student': 1})
    #
    #     # # on delete=models.CASCADE 删除外键型数据时， 不会影响主键模型的数据
    #     # student = models.StudentProfile.objects.filter(student__name="小红").delete()
    #     # print(student) # (1, {'myorm.StudentProfile': 1})
    #
    #
    #     return HttpResponse("post ok")


"""一对多"""


class ArticleView(View):
    """一对多"""

    def post(self, request: HttpRequest):
        """添加主模型，再添加外键模型"""
        # auther = models.Auther.objects.create(name="小明", age=23, sex=True)
        # article_list = [
        #     models.Article(title="标题1", content="内容1", pubdate="2025-10-01 10:10:10", auther=auther),
        #     models.Article(title="标题2", content="内容2", pubdate="2025-10-02 10:10:10", auther=auther),
        # ]
        # models.Article.objects.bulk_create(article_list)

        """先获取主模型，再添加外键模型"""
        # auther = models.Auther.objects.filter(name="小明").first()
        # if auther:
        #     article_list = [
        #         models.Article(title="标题3", content="内容3", pubdate="2025-10-03 10:10:10", auther=auther),
        #         models.Article(title="标题4", content="内容4", pubdate="2025-10-04 10:10:10", auther=auther),
        #     ]
        #     models.Article.objects.bulk_create(article_list)

        """添加数据方式二"""
        # obj = models.Article.objects.create(
        #     auther=models.Auther.objects.create(name="小红", age=21, sex=False),
        #     title="标题5",
        #     content="内容5",
        #     pubdate="2025-10-15 10:10:17"
        # )

        return HttpResponse("get ok")

    def get(self, request: HttpRequest):
        """查询数据"""
        # # 通过主模型， 查询外键模型
        # auther = models.Auther.objects.filter(name="小明").first()
        # if auther:
        #     # 获取外键 article 就是 Article.auther 中的 related_name，
        #     # 提供给 Auther 用于反向查询使用
        #     print(auther.article)  # myorm.Article.None，是因为没有调用all，所以不会执行数据库操作
        #     print(auther.article.all())  # 可以获取article数据

        """使用主模型作为条件，直接查询外键模型的数据"""
        # articles = models.Article.objects.filter(auther__name="小明").all()
        # print(articles)

        """通过外键模型查询主模型"""
        # # 例如，查询文章标题为《标题5》的作者
        # articles = models.Article.objects.filter(title="标题5")
        # if articles:
        #     print(articles) # <QuerySet [<Article: {'title': '标题5', 'content': '内容5', 'pubdate': datetime.datetime(2025, 10, 15, 10, 10, 17)}>]>
        #     print(articles[0].auther) # {'name': '小红', 'age': 21, 'sex': False}

        """使用外键模型作为条件，直接查询主模型的据"""
        # #例如，查询文章标题为《标题3》的作者
        # auther = models.Auther.objects.filter(article__title="标题3")
        # if auther:
        #     print(auther) # <QuerySet [<Auther: {'name': '小明', 'age': 23, 'sex': True}>]>

        return HttpResponse("ok")

    def put(self, request: HttpRequest):
        """更新数据 (save)"""
        # # 先获取主模型， 再改动外键模型数据， 如果外键模型有多个，需要循环修改
        # # 例如： 修改小明的文章发布日期为：2025-01-10 10:00:00
        # auther = models.Auther.objects.filter(name="小明").first()
        # if auther:
        #     for article in auther.article.all():
        #         print(article)
        #         article.pubdate = "2025-01-10 10:00:00"
        #         article.save()

        """获取到外键模型，再改动主模型"""
        # # 例如，修改文章标题《标题3》的作者为小红
        # auther = models.Auther.objects.filter(name="小红").first()
        # print(auther)
        # articles = models.Article.objects.filter(title="标题3")
        # print(articles)
        # if articles:
        #     for article in articles:
        #         article.auther = auther
        #         article.save

        # # 例如，修改文章标题《标题4》的作者的年龄为27岁
        # article = models.Article.objects.filter(title="标题4").first()
        # print(article)
        # article.auther.age = 27
        # article.auther.save()

        """更新数据 (update)"""
        # # 例如： 修改小明的标题1,标题2发布日期为：2025-02-10 10:00:00
        # # SQL:
        # # """
        # # SELECT `orm_article`.`id` FROM `orm_article`
        # # INNER JOIN `orm_auther` ON (`orm_article`.`auther_id` = `orm_auther`.`id`)
        # # WHERE (`orm_auther`.`name` = '小明' AND `orm_article`.`title` IN ('标题1', '标题2'));
        # # UPDATE `orm_article` SET `pubdate` = '2025-02-10 10:00:00' WHERE `orm_article`.`id` IN (1, 2)
        # # """
        #
        # article = models.Article.objects.filter(auther__name="小明", title__in=["标题1", "标题2"]).update(pubdate="2025-02-10 10:00:00")
        # print(article)

        # # 例如，修改文章标题《标题4》的作者的年龄为30岁
        # # SQL:
        # # """
        # # SELECT `orm_auther`.`id` FROM `orm_auther`
        # # INNER JOIN `orm_article` ON (`orm_auther`.`id` = `orm_article`.`auther_id`)
        # # WHERE `orm_article`.`title` = '标题4';
        # # UPDATE `orm_auther` SET `age` = 30 WHERE `orm_auther`.`id` IN (1)
        # # """
        #
        # auther = models.Auther.objects.filter(article__title="标题4").update(age=30)
        # print(auther)

        # # 例如，修改文章标题《标题4》的作者为小红
        # auther = models.Article.objects.filter(title="标题4").update(auther=models.Auther.objects.filter(name="小红").first())
        # print(auther)

        return HttpResponse("put ok")

    def delete(self, request: HttpRequest):
        """删除数据"""
        # on_delete = models.DO_NOTHING 不能实现，可以删除外键约束的主键
        # 当前模型的关联属性为 SET_NULL 所以，删除主模型并不会影响外键模型数据

        """
        对应的 sql 语句
        SELECT `orm_auther`.`id`, `orm_auther`.`name`, `orm_auther`.`age`, `orm_auther`.`sex` FROM `orm_auther` 
        WHERE `orm_auther`.`name` = '小红' 
        ORDER BY `orm_auther`.`id` ASC LIMIT 1
        SET AUTOCOMMIT = 0
        UPDATE `orm_article` SET `auther_id` = NULL WHERE `orm_article`.`auther_id` IN (2)
        DELETE FROM `orm_auther` WHERE `orm_auther`.`id` IN (2)
        COMMIT
        SET AUTOCOMMIT = 1
        """
        obj = models.Auther.objects.filter(name="小红").first().delete()
        print(obj)  # (1, {'myorm.Auther': 1})

        return HttpResponse("delete ok")


"""多对多"""


class TeacherView(View):
    def post(self, request: HttpRequest):
        """添加数据"""
        # # 先添加实体模型，再通过外键add绑定两个模型的关系
        # # 先创建 teacher
        # teacher = models.Teacher.objects.create(name="大明", age=30, sex=True)
        # # 创建course
        # course = models.Course.objects.create(name="python基础")
        # # 使用 add 关联 两个实体
        # teacher.course.add(course)

        # # 添加多个 course
        # # 先获取 teacher
        # teacher = models.Teacher.objects.filter(name="大明").first()
        # # 添加 course
        # courses = [
        #     models.Course.objects.create(name="python框架"),
        #     models.Course.objects.create(name="python项目实战"),
        #     models.Course.objects.create(name="python爬虫"),
        # ]
        # # 将多个 courses add 关联起来
        # teacher.course.add(*courses) # teacher.course.add(course1, course2, course3)

        return HttpResponse("post ok")

    def get(self, request: HttpRequest):
        """查询数据"""
        """先查其中一个模型，接着通过外键，查询另一个模型的数据"""
        # # 例如， 查询大明的授课列表
        # # 通过 teacher 作为条件， 查询 course
        # courses = models.Course.objects.filter(teacher__name="大明")
        # print(courses)

        # # 例如， 查询大明的授课列表
        # # 通过查询 teacher ，之后调用teacher.course.all()
        # teacher = models.Teacher.objects.filter(name="大明").first()
        # print(teacher)
        # print(teacher.course.all())

        # # 查询 哪些老师在教 python基础课
        # # 先查询 python基础，在通过外键查询老师
        # # SQL:
        # # SELECT `orm_course`.`id`, `orm_course`.`name`
        # # FROM `orm_course`
        # # WHERE `orm_course`.`name` = 'python基础'
        # # ORDER BY `orm_course`.`id` ASC LIMIT 1
        # course = models.Course.objects.filter(name="python基础").first()
        #
        # # SQL: SELECT `orm_teacher`.`id`, `orm_teacher`.`name`, `orm_teacher`.`age`, `orm_teacher`.`sex`
        # # FROM `orm_teacher` INNER JOIN `orm_course_teacher` ON (`orm_teacher`.`id` = `orm_course_teacher`.`teacher_id`)
        # # WHERE `orm_course_teacher`.`course_id` = 1 LIMIT 21
        # print(course.teacher.all())

        # # 查询 哪些老师在教 python基础课
        # # SQL:
        # # select * from orm_teacher
        # # left join orm_course_teacher on orm_teacher.id = orm_course_teacher.teacher_id
        # # left join orm_course on orm_course_teacher.course_id = orm_course.id
        # # where orm_course.name = "python基础";
        # teacher = models.Teacher.objects.filter(course__name="python基础")
        # print(teacher)

        # 查询的时候推荐使用一条语句直接查询，使用外键作为条件判断，
        # 因为在 sql 语句中，直接使用外键作为条件查询会调用 join，join 的性能会更好
        # 如果先查询课程信息，再通过课程调用外键，这样会执行两条 sql 语句，
        # 在表结构很大的情况下，使用多个 join 的性能会优于多条 select

        return HttpResponse("get ok")

    def put(self, request: HttpRequest):
        """更新数据"""
        from django.db.models import F, Q, Value
        from django.db.models.functions import Concat
        # # 把大明的所有授课课程的名字后面加上 (大明专讲)
        # courses = models.Course.objects.filter(teacher__name="大明").update(
        # # 如果不使用 Concat ，直接采用 F("name) + "(大明专讲)", 数据库的字符串拼接用的就是 concat
        # # 数据库会将 F("name) 的值转成 double 类型，导致报错
        #     name=Concat(F('name'), Value("(大明专讲)"))
        # )
        # print(courses)

        # # 把大明的所有授课课程的名字后面加上 (大明专讲) (实训循环的方式)
        # courses = models.Course.objects.filter(teacher__name="大明")
        # for course in courses:
        #     course.name = course.name + "(大明专讲)"
        #     course.save()

        return HttpResponse("put ok")

    def delete(self, request: HttpRequest):
        """删除数据"""

        # # 删除一个模型的数据，会自动删除关系表中对应的数据
        # # 例如：删除大明老师，关系表也会对应删除
        # obj = models.Teacher.objects.filter(name="大明").delete()
        # print(obj) # (5, {'myorm.Course_teacher': 4, 'myorm.Teacher': 1})

        # # 删除一个模型的数据，对应关系的一条，采用 remove 解绑的方式
        # # 例如：大红老师不教，java基础和java框架
        # teacher = models.Teacher.objects.filter(name="大红").first()
        # courses = models.Course.objects.filter(name__in=["java基础", "java框架"])
        # for course in courses:
        #     teacher.course.remove(course)

        return HttpResponse("delete ok")


"""
自关联
"""


class AreaView(View):
    def get(self, request: HttpRequest):
        """查询数据"""

        # 获取 全部区域，并打印省-市-区
        # provinces = models.Area.objects.filter(parent_id=None)
        # print(provinces)
        # citys = models.Area.objects.filter(parent__name__in=[province.name for province in provinces])
        # print(citys)
        # qus = models.Area.objects.filter(parent__parent__name__in=[province.name for province in provinces])
        # print(qus)

        # provinces = models.Area.objects.filter(parent_id=None)
        # for province in provinces:
        #     # print(province.name, end='-')
        #     for city in province.son.all():
        #         if city.son.all():
        #             for qu in city.son.all():
        #                 print(f"{province.name}-{city.name}-{qu.name}")
        #         else:
        #             print(f"{province.name}-{city.name}")

        # # 性能优化
        # from django.db.models import Prefetch
        # # 使用 prefetch_related 减少数据库查询
        # provinces = models.Area.objects.filter(parent_id=None).prefetch_related(
        #     Prefetch('son', queryset=models.Area.objects.prefetch_related('son'))
        # )
        #
        # for province in provinces:
        #     for city in province.son.all():
        #         if city.son.exists():
        #             for district in city.son.all():
        #                 print(f"{province.name}-{city.name}-{district.name}")
        #         else:
        #             print(f"{province.name}-{city.name}")

        """通过子级记录查找父级记录，得到唯一的父级"""
        # area = models.Area.objects.filter(name="二七区").first()
        # print(area.parent)  # {'id': 3, 'name': '郑州市'}
        # print(area.parent.parent)  # {'id': 1, 'name': '河南省'}

        """通过父级记录查找子级记录，得到多个子级"""
        # province = models.Area.objects.filter(name="河南省").first()
        # citys = province.son.all()
        # print(citys)  # <QuerySet [<Area: {'id': 3, 'name': '郑州市'}>, <Area: {'id': 4, 'name': '开封市'}>]>
        # for city in citys:
        #     print(city.name, city.son.all())

        """使用子级记录作为查询条件，查询数据"""
        # # 查询 二七区 是哪个省份的，因为是区级，所以 son__son__name="二七区"
        # area = models.Area.objects.filter(son__son__name="二七区")
        # print(area)  # <QuerySet [<Area: {'id': 1, 'name': '河南省'}>]>

        # # 查询 深圳市 是哪个省份的，因为是市级，所以 son__name="深圳市"
        # area = models.Area.objects.filter(son__name="深圳市")
        # print(area)  # <QuerySet [<Area: {'id': 10, 'name': '广东省'}>]>

        """使用父级记录作为查询条件，查询数据"""
        # # 查询哪些市级的省份是 河南省
        # area = models.Area.objects.filter(parent__name="河南省")
        # print(area)  # <QuerySet [<Area: {'id': 3, 'name': '郑州市'}>, <Area: {'id': 4, 'name': '开封市'}>]>

        # # 查询 河南省 有哪些区域
        # area = models.Area.objects.filter(parent__parent__name="河南省")
        # print(area)  # <QuerySet [<Area: {'id': 7, 'name': '二七区'}>, <Area: {'id': 8, 'name': '新郑区'}>, <Area: {'id': 9, 'name': '郑东新区'}>]>
        #

        # from django.db import connections
        # with connections["default"].cursor() as cursor:
        #     # 让游标执行SQL语句
        #     cursor.execute("""
        #                    select t1.name as 省, t2.name as 市, t3.name as 区
        #                    from orm_area t1
        #                             left join orm_area t2 on t2.parent_id = t1.id
        #                             left join orm_area t3 on t3.parent_id = t2.id
        #                    where t1.parent_id is null
        #                    """)
        #     # 通过游标获取查询结果
        #     result = cursor.fetchall()
        #     # print(result)
        #     for r in result:
        #         print(r)

        return HttpResponse("area get ok")

    def post(self, request: HttpRequest):
        """添加数据"""
        # # # 添加省份数据，因为没有上级辖区，所以不需要声明其他字段
        # area1 = models.Area.objects.create(name="河南省")
        # area2 = models.Area.objects.create(name="河北省")
        # # 添加城市
        # area1.son.add(
        #     models.Area.objects.create(name="郑州市"),
        #     models.Area.objects.create(name="开封市"),
        # )
        #
        # models.Area.objects.create(name="石家庄", parent=area2)
        # models.Area.objects.create(name="邯郸市", parent_id=area2.id)
        #
        # # 添加地区数据
        # area5 = models.Area.objects.get(name="郑州市")
        # area5.son.add(*[
        #     models.Area.objects.create(name="二七区"),
        #     models.Area.objects.create(name="新郑区"),
        #     models.Area.objects.create(name="郑东新区"),
        # ])

        # mysql> select * from orm_area;
        # +----+--------------+-----------+
        # | id | name         | parent_id |
        # +----+--------------+-----------+
        # |  1 | 河南省       |      NULL |
        # |  2 | 河北省       |      NULL |
        # |  3 | 郑州市       |         1 |
        # |  4 | 开封市       |         1 |
        # |  5 | 石家庄       |         2 |
        # |  6 | 邯郸市       |         2 |
        # |  7 | 二七区       |         3 |
        # |  8 | 新郑区       |         3 |
        # |  9 | 郑东新区     |         3 |
        # +----+--------------+-----------+

        # province = models.Area.objects.create(name="广东省")
        # area_list = [
        #     models.Area(name="佛山市"),
        #     models.Area(name="广州市"),
        #     models.Area(name="珠海市"),
        #     models.Area(name="深圳市"),
        # ]
        # # bulk属性只有在一对多的时候存在，多对多是没有。
        # # bulk允许列表中出现没有保存到数据库中的模型对象，django会自动创建到数据库中
        # province.son.add(*area_list, bulk=False)

        # mysql> select * from orm_area;
        # +----+--------------+-----------+
        # | id | name         | parent_id |
        # +----+--------------+-----------+
        # |  1 | 河南省       |      NULL |
        # |  2 | 河北省       |      NULL |
        # |  3 | 郑州市       |         1 |
        # |  4 | 开封市       |         1 |
        # |  5 | 石家庄       |         2 |
        # |  6 | 邯郸市       |         2 |
        # |  7 | 二七区       |         3 |
        # |  8 | 新郑区       |         3 |
        # |  9 | 郑东新区     |         3 |
        # | 10 | 广东省       |      NULL |
        # | 11 | 佛山市       |        10 |
        # | 12 | 广州市       |        10 |
        # | 13 | 珠海市       |        10 |
        # | 14 | 深圳市       |        10 |
        # +----+--------------+-----------+

        return HttpResponse("area post ok")


class PeopleView(View):
    def get(self, request: HttpRequest):
        """查询数据"""

        # # 查询哪些人是小黑的朋友
        # people = models.People.objects.filter(name="小黑").first()
        # print(people.friends.all())

        # peoples = models.People.objects.all()
        # print(peoples)
        # for people in peoples:
        #     print(people)
        #     print(people.friends.all())
        return HttpResponse("get ok")

    def post(self, request: HttpRequest):
        """添加数据"""
        # # 添加人的数据
        # p1 = models.People.objects.create(name="小明")
        # p2 = models.People.objects.create(name="小红")
        # p3 = models.People.objects.create(name="小白")
        # p4 = models.People.objects.create(name="小黑")
        # p5 = models.People.objects.create(name="小兰")
        #
        # # 小红添加好友 (小明，小黑)
        # p_hong = models.People.objects.get(name="小红")
        # p_ming = models.People.objects.get(name="小明")
        # p_hei = models.People.objects.get(name="小黑")
        # p_hong.friends.add(p_ming, p_hei)
        #
        # # 小明添加好友
        # p_ming = models.People.objects.get(name="小明")
        # p_hei = models.People.objects.get(name="小黑")
        # p_bai = models.People.objects.get(name="小白")
        # p_hone = models.People.objects.get(name="小红")
        # p_ming.friends.add(p_hei, p_bai, p_hone)
        #
        # # 小兰添加好友
        # p_lan = models.People.objects.get(name="小兰")
        # p_hei = models.People.objects.get(name="小黑")
        # p_bai = models.People.objects.get(name="小白")
        # p_hone = models.People.objects.get(name="小红")
        # p_ming = models.People.objects.get(name="小明")
        # p_lan.friends.add(p_hei, p_bai, p_hone, p_ming)
        #
        # # 小白添加好友
        # p_bai = models.People.objects.get(name="小白")
        # p_hei = models.People.objects.get(name="小黑")
        # p_ming = models.People.objects.get(name="小明")
        # p_hone = models.People.objects.get(name="小红")
        # p_bai.friends.add(p_hei, p_ming, p_hone)

        return HttpResponse("people post ok")


"""
使用 select_related()  /  prefetch_related() 对查询进行优化

        select_related() vs prefetch_related() 的区别
核心区别
特性	        select_related()	            prefetch_related()
工作原理	    使用 SQL JOIN 语句	            使用分开的查询 + Python 内存关联
查询次数	    1 次查询	                    2 次或更多查询
适用关系	    ForeignKey, OneToOneField	    ManyToManyField, 反向 ForeignKey
性能特点	    JOIN 可能复杂但单次	        多个简单查询
内存使用	    可能返回冗余数据	            更高效的数据结构

select_related() 适合：

# 一对一关系
Person.objects.select_related('profile')

# 多对一关系（外键）
Article.objects.select_related('author')

# 链式关系
Article.objects.select_related('author__profile')


prefetch_related() 适合：

# 多对多关系
Person.objects.prefetch_related('groups')

# 反向外键关系
Author.objects.prefetch_related('article_set')

# 复杂预取
Person.objects.prefetch_related(
    Prefetch('groups', queryset=Group.objects.filter(active=True))
)

"""


class YouHuaSearchView(View):
    def get(self, request: HttpRequest):
        """[查询优化] select_related"""
        """获取张三丰的居住地"""
        # # 不使用 select_related
        # person = models.Person.objects.filter(firstname="张", lastname="三丰").first()
        # print(person.living.name) # 需要两条sql语句
        # # """
        # # SELECT `tb_person`.`id`, `tb_person`.`firstname`, `tb_person`.`lastname`, `tb_person`.`hometown_id`, `tb_person`.`living_id`
        # # FROM `tb_person` WHERE (`tb_person`.`firstname` = '张' AND `tb_person`.`lastname` = '三丰') ORDER BY `tb_person`.`id` ASC LIMIT 1
        # # SELECT `tb_city`.`id`, `tb_city`.`name`, `tb_city`.`province_id` FROM `tb_city` WHERE `tb_city`.`id` = 1 LIMIT 21
        # # """

        # # select_related 全外键关联优化
        # person = models.Person.objects.filter(firstname="张", lastname="三丰").select_related().first()
        # # """
        # # SELECT `tb_person`.`id`, `tb_person`.`firstname`, `tb_person`.`lastname`, `tb_person`.`hometown_id`, `tb_person`.`living_id` FROM `tb_person` WHERE (`tb_person`.`firstname` = '张' AND `tb_person`.`lastname` = '三丰') ORDER BY `tb_person`.`id` ASC LIMIT 1
        # # """

        # # 限定外键的优化查找
        # person = models.Person.objects.filter(firstname="张", lastname="三丰").select_related("living").first()
        # print(person.living.name) # 只需要一条sql语句
        # # """
        # # SELECT `tb_person`.`id`, `tb_person`.`firstname`, `tb_person`.`lastname`, `tb_person`.`hometown_id`, `tb_person`.`living_id`, `tb_city`.`id`, `tb_city`.`name`, `tb_city`.`province_id`
        # # FROM `tb_person`
        # # LEFT OUTER JOIN `tb_city` ON (`tb_person`.`living_id` = `tb_city`.`id`)
        # # WHERE (`tb_person`.`firstname` = '张' AND `tb_person`.`lastname` = '三丰')
        # # ORDER BY `tb_person`.`id` ASC LIMIT 1
        # # """

        """获取张三丰的居住地和省份"""
        # person = models.Person.objects.filter(firstname="张", lastname="三丰").select_related("living").select_related("living__province")
        # # """
        # # SELECT `tb_person`.`id`,
        # #        `tb_person`.`firstname`,
        # #        `tb_person`.`lastname`,
        # #        `tb_person`.`hometown_id`,
        # #        `tb_person`.`living_id`,
        # #        `tb_city`.`id`,
        # #        `tb_city`.`name`,
        # #        `tb_city`.`province_id`,
        # #        `tb_province`.`id`,
        # #        `tb_province`.`name`
        # # FROM `tb_person`
        # #          LEFT OUTER JOIN `tb_city` ON (`tb_person`.`living_id` = `tb_city`.`id`)
        # #          LEFT OUTER JOIN `tb_province` ON (`tb_city`.`province_id` = `tb_province`.`id`)
        # # WHERE (`tb_person`.`firstname` = '张' AND `tb_person`.`lastname` = '三丰') LIMIT 21
        # # """

        # # 等同于上一段代码

        # person = models.Person.objects.filter(firstname="张", lastname="三丰").select_related("living__province")
        # # """
        # # SELECT `tb_person`.`id`,
        # #        `tb_person`.`firstname`,
        # #        `tb_person`.`lastname`,
        # #        `tb_person`.`hometown_id`,
        # #        `tb_person`.`living_id`,
        # #        `tb_city`.`id`,
        # #        `tb_city`.`name`,
        # #        `tb_city`.`province_id`,
        # #        `tb_province`.`id`,
        # #        `tb_province`.`name`
        # # FROM `tb_person`
        # #          LEFT OUTER JOIN `tb_city` ON (`tb_person`.`living_id` = `tb_city`.`id`)
        # #          LEFT OUTER JOIN `tb_province` ON (`tb_city`.`province_id` = `tb_province`.`id`)
        # # WHERE (`tb_person`.`firstname` = '张' AND `tb_person`.`lastname` = '三丰') LIMIT 21
        # # """
        # print(person[0].living.name, person[0].living.province.name)

        """
        [查询优化] prefetch_related
        """

        # # 查询所有人的足迹 (使用原来的方法)
        # persons = models.Person.objects.all()
        # for person in persons:
        #     print(person.visitation.all())
        # # 使用for循环，要执行sql查询语句这么多次
        # # """
        # # SELECT `tb_person`.`id`, `tb_person`.`firstname`, `tb_person`.`lastname`, `tb_person`.`hometown_id`, `tb_person`.`living_id` FROM `tb_person`
        # # SELECT `tb_city`.`id`, `tb_city`.`name`, `tb_city`.`province_id` FROM `tb_city` INNER JOIN `tb_person_visitation` ON (`tb_city`.`id` = `tb_person_visitation`.`city_id`) WHERE `tb_person_visitation`.`person_id` = 1 LIMIT 21
        # # SELECT `tb_city`.`id`, `tb_city`.`name`, `tb_city`.`province_id` FROM `tb_city` INNER JOIN `tb_person_visitation` ON (`tb_city`.`id` = `tb_person_visitation`.`city_id`) WHERE `tb_person_visitation`.`person_id` = 2 LIMIT 21
        # # SELECT `tb_city`.`id`, `tb_city`.`name`, `tb_city`.`province_id` FROM `tb_city` INNER JOIN `tb_person_visitation` ON (`tb_city`.`id` = `tb_person_visitation`.`city_id`) WHERE `tb_person_visitation`.`person_id` = 3 LIMIT 21
        # # SELECT `tb_city`.`id`, `tb_city`.`name`, `tb_city`.`province_id` FROM `tb_city` INNER JOIN `tb_person_visitation` ON (`tb_city`.`id` = `tb_person_visitation`.`city_id`) WHERE `tb_person_visitation`.`person_id` = 4 LIMIT 21
        # # SELECT `tb_city`.`id`, `tb_city`.`name`, `tb_city`.`province_id` FROM `tb_city` INNER JOIN `tb_person_visitation` ON (`tb_city`.`id` = `tb_person_visitation`.`city_id`) WHERE `tb_person_visitation`.`person_id` = 5 LIMIT 21
        # # """

        # # 使用 prefetch_related 优化
        #
        # persons = models.Person.objects.all().prefetch_related("visitation")
        # for person in persons:
        #     print(person.visitation.all())
        # # 同样是使用循环，只执行了两次sql语句查询
        # # """
        # # SELECT `tb_person`.`id`, `tb_person`.`firstname`, `tb_person`.`lastname`, `tb_person`.`hometown_id`, `tb_person`.`living_id` FROM `tb_person`
        # # SELECT (`tb_person_visitation`.`person_id`) AS `_prefetch_related_val_person_id`, `tb_city`.`id`, `tb_city`.`name`, `tb_city`.`province_id` FROM `tb_city` INNER JOIN `tb_person_visitation` ON (`tb_city`.`id` = `tb_person_visitation`.`city_id`) WHERE `tb_person_visitation`.`person_id` IN (1, 2, 3, 4, 5)
        # # """

        # # prefetch_related 也支持多级外键的处理
        # # 例如：查询所有人去过的省份
        # persons = models.Person.objects.all().prefetch_related("visitation__province")
        # for person in persons:
        #     for vis in person.visitation.all():
        #         print(person.firstname + person.lastname, vis.name, vis.province.name)
        #
        # # 只需要查询三次数据库即可
        # # """
        # # SELECT `tb_person`.`id`, `tb_person`.`firstname`, `tb_person`.`lastname`, `tb_person`.`hometown_id`, `tb_person`.`living_id` FROM `tb_person`
        # # SELECT (`tb_person_visitation`.`person_id`) AS `_prefetch_related_val_person_id`, `tb_city`.`id`, `tb_city`.`name`, `tb_city`.`province_id` FROM `tb_city` INNER JOIN `tb_person_visitation` ON (`tb_city`.`id` = `tb_person_visitation`.`city_id`) WHERE `tb_person_visitation`.`person_id` IN (1, 2, 3, 4, 5)
        # # SELECT `tb_province`.`id`, `tb_province`.`name` FROM `tb_province` WHERE `tb_province`.`id` IN (1, 2)
        # # """

        """以下情况不推荐使用，必须使用 prefetch_related 优化"""
        # persons = models.Person.objects.all()
        # for person in persons:
        #     visitations = models.City.objects.filter(person_visitation__id=person.id).all()
        #     for visitation in visitations:
        #         province = models.Province.objects.filter(city__name=visitation.name).first()
        #         print(person.firstname+person.lastname, visitation.name, province.name)
        #
        # # 这种方法要 查询如下次数，所以不推荐
        # """
        # SELECT `tb_person`.`id`, `tb_person`.`firstname`, `tb_person`.`lastname`, `tb_person`.`hometown_id`, `tb_person`.`living_id` FROM `tb_person`
        # SELECT `tb_city`.`id`, `tb_city`.`name`, `tb_city`.`province_id` FROM `tb_city` INNER JOIN `tb_person_visitation` ON (`tb_city`.`id` = `tb_person_visitation`.`city_id`) WHERE `tb_person_visitation`.`person_id` = 1
        # SELECT `tb_province`.`id`, `tb_province`.`name` FROM `tb_province` INNER JOIN `tb_city` ON (`tb_province`.`id` = `tb_city`.`province_id`) WHERE `tb_city`.`name` = '开封市' ORDER BY `tb_province`.`id` ASC LIMIT 1
        # SELECT `tb_province`.`id`, `tb_province`.`name` FROM `tb_province` INNER JOIN `tb_city` ON (`tb_province`.`id` = `tb_city`.`province_id`) WHERE `tb_city`.`name` = '郑州市' ORDER BY `tb_province`.`id` ASC LIMIT 1
        # SELECT `tb_province`.`id`, `tb_province`.`name` FROM `tb_province` INNER JOIN `tb_city` ON (`tb_province`.`id` = `tb_city`.`province_id`) WHERE `tb_city`.`name` = '广州市' ORDER BY `tb_province`.`id` ASC LIMIT 1
        # SELECT `tb_city`.`id`, `tb_city`.`name`, `tb_city`.`province_id` FROM `tb_city` INNER JOIN `tb_person_visitation` ON (`tb_city`.`id` = `tb_person_visitation`.`city_id`) WHERE `tb_person_visitation`.`person_id` = 2
        # SELECT `tb_province`.`id`, `tb_province`.`name` FROM `tb_province` INNER JOIN `tb_city` ON (`tb_province`.`id` = `tb_city`.`province_id`) WHERE `tb_city`.`name` = '郑州市' ORDER BY `tb_province`.`id` ASC LIMIT 1
        # SELECT `tb_province`.`id`, `tb_province`.`name` FROM `tb_province` INNER JOIN `tb_city` ON (`tb_province`.`id` = `tb_city`.`province_id`) WHERE `tb_city`.`name` = '广州市' ORDER BY `tb_province`.`id` ASC LIMIT 1
        # SELECT `tb_province`.`id`, `tb_province`.`name` FROM `tb_province` INNER JOIN `tb_city` ON (`tb_province`.`id` = `tb_city`.`province_id`) WHERE `tb_city`.`name` = '深圳市' ORDER BY `tb_province`.`id` ASC LIMIT 1
        # SELECT `tb_city`.`id`, `tb_city`.`name`, `tb_city`.`province_id` FROM `tb_city` INNER JOIN `tb_person_visitation` ON (`tb_city`.`id` = `tb_person_visitation`.`city_id`) WHERE `tb_person_visitation`.`person_id` = 3
        # SELECT `tb_province`.`id`, `tb_province`.`name` FROM `tb_province` INNER JOIN `tb_city` ON (`tb_province`.`id` = `tb_city`.`province_id`) WHERE `tb_city`.`name` = '开封市' ORDER BY `tb_province`.`id` ASC LIMIT 1
        # SELECT `tb_province`.`id`, `tb_province`.`name` FROM `tb_province` INNER JOIN `tb_city` ON (`tb_province`.`id` = `tb_city`.`province_id`) WHERE `tb_city`.`name` = '郑州市' ORDER BY `tb_province`.`id` ASC LIMIT 1
        # SELECT `tb_province`.`id`, `tb_province`.`name` FROM `tb_province` INNER JOIN `tb_city` ON (`tb_province`.`id` = `tb_city`.`province_id`) WHERE `tb_city`.`name` = '广州市' ORDER BY `tb_province`.`id` ASC LIMIT 1
        # SELECT `tb_province`.`id`, `tb_province`.`name` FROM `tb_province` INNER JOIN `tb_city` ON (`tb_province`.`id` = `tb_city`.`province_id`) WHERE `tb_city`.`name` = '深圳市' ORDER BY `tb_province`.`id` ASC LIMIT 1
        # SELECT `tb_city`.`id`, `tb_city`.`name`, `tb_city`.`province_id` FROM `tb_city` INNER JOIN `tb_person_visitation` ON (`tb_city`.`id` = `tb_person_visitation`.`city_id`) WHERE `tb_person_visitation`.`person_id` = 4
        # SELECT `tb_province`.`id`, `tb_province`.`name` FROM `tb_province` INNER JOIN `tb_city` ON (`tb_province`.`id` = `tb_city`.`province_id`) WHERE `tb_city`.`name` = '广州市' ORDER BY `tb_province`.`id` ASC LIMIT 1
        # SELECT `tb_province`.`id`, `tb_province`.`name` FROM `tb_province` INNER JOIN `tb_city` ON (`tb_province`.`id` = `tb_city`.`province_id`) WHERE `tb_city`.`name` = '深圳市' ORDER BY `tb_province`.`id` ASC LIMIT 1
        # SELECT `tb_city`.`id`, `tb_city`.`name`, `tb_city`.`province_id` FROM `tb_city` INNER JOIN `tb_person_visitation` ON (`tb_city`.`id` = `tb_person_visitation`.`city_id`) WHERE `tb_person_visitation`.`person_id` = 5
        # SELECT `tb_province`.`id`, `tb_province`.`name` FROM `tb_province` INNER JOIN `tb_city` ON (`tb_province`.`id` = `tb_city`.`province_id`) WHERE `tb_city`.`name` = '郑州市' ORDER BY `tb_province`.`id` ASC LIMIT 1
        # SELECT `tb_province`.`id`, `tb_province`.`name` FROM `tb_province` INNER JOIN `tb_city` ON (`tb_province`.`id` = `tb_city`.`province_id`) WHERE `tb_city`.`name` = '广州市' ORDER BY `tb_province`.`id` ASC LIMIT 1
        # SELECT `tb_province`.`id`, `tb_province`.`name` FROM `tb_province` INNER JOIN `tb_city` ON (`tb_province`.`id` = `tb_city`.`province_id`) WHERE `tb_city`.`name` = '深圳市' ORDER BY `tb_province`.`id` ASC LIMIT 1
        # """

        # # 使用Prefetch 对象优化
        # # 主要优化点：
        # # 使用 Prefetch 对象进行精确控制
        # # 使用 select_related 在预取时连接省份表
        # # 使用 only() 限制查询字段
        # from django.db.models import Prefetch
        # persons = models.Person.objects.only("firstname", "lastname").prefetch_related(
        #     Prefetch(
        #         "visitation",
        #         queryset=models.City.objects.select_related("province").only("name", "province__name")
        #     )
        # )
        # for person in persons:
        #     for vis in person.visitation.all():
        #         print(person.firstname + person.lastname, vis.name, vis.province.name)
        #
        # # """
        # # SELECT `tb_person`.`id`, `tb_person`.`firstname`, `tb_person`.`lastname` FROM `tb_person`
        # # SELECT (`tb_person_visitation`.`person_id`) AS `_prefetch_related_val_person_id`, `tb_city`.`id`, `tb_city`.`name`, `tb_city`.`province_id`, `tb_province`.`id`, `tb_province`.`name`
        # # FROM `tb_city`
        # # INNER JOIN `tb_person_visitation` ON (`tb_city`.`id` = `tb_person_visitation`.`city_id`)
        # # LEFT OUTER JOIN `tb_province` ON (`tb_city`.`province_id` = `tb_province`.`id`)
        # # WHERE `tb_person_visitation`.`person_id` IN (1, 2, 3, 4, 5)
        # # """

        # # 查询 哪个人的hometown在 广东省
        # persons = models.Person.objects.filter(hometown__province__name="广东省")

        # # # 查询 在广东省旅游的人的手机号，（visitation 在 广东省 的人的电话号）
        # persons = models.Person.objects.filter(visitation__province__name="广东省").select_related("profile").distinct()
        # for person in persons:
        #     print(person, person.profile.mobile)
        #
        # # 如果有的 Person 不存在 PersonProfile，使用如下方法
        # profiles = models.PersonProfile.objects.select_related("person").filter(person__visitation__province__name="广东省").distinct()
        # for profile in profiles:
        #     print(profile.mobile, profile.person)
        # print(persons)

        # 张无忌的家乡在哪个省份哪个城市？
        # 张无忌的老乡都有谁？
        # 张无忌都去过了哪些城市？
        # 张三丰与张无忌有没有去过同样的城市？如果有，都有哪些城市？

        # # 张无忌的家乡在哪个省份哪个城市？
        # person = models.Person.objects.filter(firstname="张", lastname="无忌").select_related("hometown__province").first()
        #
        # # print(person[0].hometown.province.name, person[0].hometown.name) # 使用 person[0] 两次，每次都会触发数据库查询
        # # 所以在确认结果唯一的情况下，使用 first() 或者使用 get 过滤数据，这样读取数据的时候会减少数据的查询次数
        # print(person.hometown.province.name, person.hometown.name)

        # # 张无忌的老乡都有谁？
        # zwj_hometown_id = models.Person.objects.only('hometown_id').get(firstname="张", lastname="无忌").hometown_id
        # if zwj_hometown_id:
        #     persons = models.Person.objects.filter(hometown_id=zwj_hometown_id).exclude(
        #         firstname="张", lastname="无忌"
        #     )
        #     print(persons)

        # 张无忌都去过了哪些城市？
        # from django.db.models import Q
        # zwj_id = models.Person.objects.only("id").get(firstname="张", lastname="无忌").id
        # citys = models.City.objects.filter(Q(person_hometown__id=zwj_id) | Q(person_visitation__id=zwj_id) | Q(person_living__id=zwj_id)).distinct()
        # print(citys)

        # # from django.db.models import Q
        # #
        # # 使用单个查询获取所有相关城市
        # citys = models.City.objects.filter(
        #     Q(person_visitation__firstname="张", person_visitation__lastname="无忌") |
        #     Q(person_hometown__firstname="张", person_hometown__lastname="无忌") |
        #     Q(person_living__firstname="张", person_living__lastname="无忌")
        # ).distinct()
        # print(citys)



        # # 张三丰与张无忌有没有去过同样的城市？如果有，都有哪些城市？
        # from django.db.models import Q
        # # 分别查询然后取交集
        # zwj_cities  = models.City.objects.filter(
        #     Q(person_visitation__firstname="张", person_visitation__lastname="无忌")
        # )
        # zsf_cities = models.City.objects.filter(
        #     Q(person_visitation__firstname="张", person_visitation__lastname="三丰")
        # )
        #
        # common_cities = zwj_cities & zsf_cities
        # """
        # SELECT `tb_city`.`id`, `tb_city`.`name`, `tb_city`.`province_id`
        # FROM `tb_city`
        #          INNER JOIN `tb_person_visitation` ON (`tb_city`.`id` = `tb_person_visitation`.`city_id`)
        #          INNER JOIN `tb_person` ON (`tb_person_visitation`.`person_id` = `tb_person`.`id`)
        #          LEFT OUTER JOIN `tb_person_visitation` T4 ON (`tb_city`.`id` = T4.`city_id`)
        #          LEFT OUTER JOIN `tb_person` T5 ON (T4.`person_id` = T5.`id`)
        # WHERE (`tb_person`.`firstname` = '张' AND `tb_person`.`lastname` = '无忌' AND T5.`firstname` = '张' AND
        #        T5.`lastname` = '三丰') LIMIT 21
        # """
        #
        # print(common_cities)


        return JsonResponse({"msg": "get ok"})
