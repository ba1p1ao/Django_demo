from wsgiref.util import application_uri

from django.shortcuts import render
from django.views import View
from django.http import HttpResponse, HttpRequest
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