from django.db import models


class Author(models.Model):
    """
    作者模型
    存储作者的基本信息，与书籍模型为一对多关系（一个作者可有多本书）
    """
    name = models.CharField(max_length=100, verbose_name="作者姓名")  # 作者姓名，最大长度100
    email = models.EmailField(verbose_name="电子邮箱")  # 作者电子邮箱，符合邮箱格式验证
    bio = models.TextField(verbose_name="作者简介")  # 作者详细简介，无长度限制
    birth_date = models.DateField(verbose_name="出生日期")  # 作者出生日期
    is_active = models.BooleanField(default=True, verbose_name="是否活跃")  # 作者状态，默认活跃

    class Meta:
        db_table = "test_author"  # 数据库表名
        verbose_name = "作者"  # 后台管理显示名称（单数）
        verbose_name_plural = "作者列表"  # 后台管理显示名称（复数）

    def __str__(self):
        return self.name  # 实例打印时返回作者姓名


class Publisher(models.Model):
    """
    出版社模型
    存储出版社的基本信息，与书籍模型为一对多关系（一个出版社可出版多本书）
    """
    name = models.CharField(max_length=200, verbose_name="出版社名称")  # 出版社名称，最大长度200
    address = models.TextField(verbose_name="出版社地址")  # 出版社详细地址，无长度限制
    website = models.URLField(verbose_name="官方网站")  # 出版社官网URL，符合URL格式验证
    founded_year = models.IntegerField(verbose_name="成立年份")  # 出版社成立年份

    class Meta:
        db_table = "test_publisher"  # 数据库表名
        verbose_name = "出版社"  # 后台管理显示名称（单数）
        verbose_name_plural = "出版社列表"  # 后台管理显示名称（复数）

    def __str__(self):
        return self.name  # 实例打印时返回出版社名称


class Book(models.Model):
    """
    书籍模型
    存储书籍的核心信息，关联作者、出版社，与评论模型为一对多关系，与书店模型为多对多关系（通过库存模型关联）
    """
    GENRE_CHOICES = [
        ('FIC', '小说'),
        ('SCI', '科幻'),
        ('MYS', '悬疑'),
        ('BIO', '传记'),
        ('HIS', '历史'),
        ('SCI', '科学'),
    ]  # 书籍类型选项集（存储值，显示值）

    title = models.CharField(max_length=200, verbose_name="书籍标题")  # 书籍名称，最大长度200
    isbn = models.CharField(max_length=13, unique=True, verbose_name="ISBN编号")  # 国际标准书号，唯一标识
    publication_date = models.DateField(verbose_name="出版日期")  # 书籍出版日期
    price = models.DecimalField(max_digits=6, decimal_places=2, verbose_name="售价")  # 书籍售价，最大6位数字（含2位小数）
    pages = models.IntegerField(verbose_name="页数")  # 书籍总页数
    genre = models.CharField(max_length=3, choices=GENRE_CHOICES, verbose_name="书籍类型")  # 书籍类型，关联选项集
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='books',
                               verbose_name="作者")  # 关联作者（级联删除）
    publisher = models.ForeignKey(Publisher, on_delete=models.CASCADE, related_name='books',
                                  verbose_name="出版社")  # 关联出版社（级联删除）

    class Meta:
        db_table = "test_book"  # 数据库表名
        verbose_name = "书籍"  # 后台管理显示名称（单数）
        verbose_name_plural = "书籍列表"  # 后台管理显示名称（复数）

    def __str__(self):
        return self.title  # 实例打印时返回书籍标题


class Review(models.Model):
    """
    书籍评论模型
    存储书籍的用户评论信息，与书籍模型为一对多关系（一本书可有多条评论）
    """
    RATING_CHOICES = [
        (1, '1星'),
        (2, '2星'),
        (3, '3星'),
        (4, '4星'),
        (5, '5星'),
    ]  # 评分选项集（存储值，显示值）

    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='reviews',
                             verbose_name="关联书籍")  # 关联书籍（级联删除）
    reviewer_name = models.CharField(max_length=100, verbose_name="评论者姓名")  # 评论者姓名，最大长度100
    rating = models.IntegerField(choices=RATING_CHOICES, verbose_name="评分")  # 书籍评分，关联评分选项集
    comment = models.TextField(verbose_name="评论内容")  # 评论详细内容，无长度限制
    review_date = models.DateTimeField(auto_now_add=True, verbose_name="评论时间")  # 评论提交时间，自动记录创建时间
    is_verified = models.BooleanField(default=False, verbose_name="是否已验证")  # 评论验证状态，默认未验证

    class Meta:
        db_table = "test_review"  # 数据库表名
        verbose_name = "书籍评论"  # 后台管理显示名称（单数）
        verbose_name_plural = "书籍评论列表"  # 后台管理显示名称（复数）

    def __str__(self):
        return f"{self.reviewer_name} - {self.book.title}"  # 实例打印时返回"评论者-书籍名"格式


class BookStore(models.Model):
    """
    书店模型
    存储书店的基本信息，与书籍模型为多对多关系（通过Inventory中间表关联，一个书店可售多本书，一本书可在多个书店销售）
    """
    name = models.CharField(max_length=100, verbose_name="书店名称")  # 书店名称，最大长度100
    location = models.CharField(max_length=200, verbose_name="书店地址")  # 书店地址，最大长度200
    books = models.ManyToManyField(Book, through='Inventory', related_name='bookstores',
                                   verbose_name="关联书籍")  # 多对多关联书籍，通过Inventory中间表

    class Meta:
        db_table = "test_book_store"  # 数据库表名
        verbose_name = "书店"  # 后台管理显示名称（单数）
        verbose_name_plural = "书店列表"  # 后台管理显示名称（复数）

    def __str__(self):
        return self.name  # 实例打印时返回书店名称


class Inventory(models.Model):
    """
    库存模型（多对多中间表）
    关联书店和书籍，存储每本书在对应书店的库存信息，是Book与BookStore的多对多关联中间表
    """
    book = models.ForeignKey(Book, on_delete=models.CASCADE, verbose_name="关联书籍")  # 关联书籍（级联删除）
    bookstore = models.ForeignKey(BookStore, on_delete=models.CASCADE, verbose_name="关联书店")  # 关联书店（级联删除）
    quantity = models.IntegerField(default=0, verbose_name="库存数量")  # 书籍在该书店的库存数量，默认0
    last_restocked = models.DateTimeField(auto_now=True, verbose_name="最后补货时间")  # 最后补货时间，自动记录更新时间

    class Meta:
        db_table = "test_inventory"  # 数据库表名
        unique_together = ['book', 'bookstore']  # 联合唯一约束：同一本书在同一书店只能有一条库存记录
        verbose_name = "库存记录"  # 后台管理显示名称（单数）
        verbose_name_plural = "库存记录列表"  # 后台管理显示名称（复数）

    def __str__(self):
        return f"{self.bookstore.name} - {self.book.title}（库存：{self.quantity}）"  # 实例打印时返回"书店名-书籍名（库存数）"格式

from django.db.models import Manager

class MyManager(Manager):
    """继承了Manager，objects就会有以下方法，方便数据库模型直接调用"""
    def get_access_user(self):
        """获取成年人列表"""
        return self.filter(age__gte=18)

class ModelDemo(models.Model):
    name = models.CharField(max_length=20, db_index=True, verbose_name="姓名")
    age = models.IntegerField(verbose_name="年龄")
    sex = models.BooleanField(default=False, verbose_name="性别")
    objects = MyManager() # 重写objects函数，该阐述会影响到view中模型调用objects方法
    # 如果 objects2 = MyManager()，后续就要使用模型调用objects2



    class Meta:
        db_table = "model_demo"
        verbose_name = db_table
        verbose_name_plural = verbose_name


    def __str__(self):
        return self.name


    # 不推荐这样写，虽然说可以实现功能，但是导致了，代码结构不规范，分不清楚
    # 调用的是模型类还是自己写的类
    @classmethod
    def get_access_user(cls):
        """获取成年人列表"""

        return cls.objects.filter(age__gte=18)



# 抽象模型：保存一些公共字段或者公共属性方法。
# 数据模型：对应数据库的表结构
# 代理模型：


# 代理模型
class FemaleUser(ModelDemo):
    class Meta:
        proxy = True # 设置当前模型为代理模型，共烹父模型的数据和操作方法

    @classmethod
    def all(cls):
        return cls.objects.filter(sex=True)


class MaleUser(ModelDemo):
    class Meta:
        proxy = True

    @classmethod
    def all(cls):
        return cls.objects.filter(sex=False)


