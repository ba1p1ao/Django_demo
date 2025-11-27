from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.views import View
from django.db import connection
from django.db.models import Count, Avg, Max, Prefetch
import time
from myormlianxi import models


class BookView(View):
    def post(self, request):
        # 删除现有数据（按正确顺序删除以避免外键约束错误）
        models.Inventory.objects.all().delete()
        models.Review.objects.all().delete()
        models.BookStore.objects.all().delete()
        models.Book.objects.all().delete()
        models.Author.objects.all().delete()
        models.Publisher.objects.all().delete()

        # 创建作者并保存到数据库
        authors = [
            models.Author(name="刘慈欣", email="liucixin@email.com", bio="著名科幻作家", birth_date="1963-06-23"),
            models.Author(name="余华", email="yuhua@email.com", bio="当代著名作家", birth_date="1960-04-03"),
            models.Author(name="莫言", email="moyan@email.com", bio="诺贝尔文学奖获得者", birth_date="1955-02-17"),
            models.Author(name="东野圭吾", email="higashino@email.com", bio="日本推理小说作家",
                          birth_date="1958-02-04"),
        ]
        # 逐个保存作者以获取ID
        saved_authors = []
        for author in authors:
            author.save()
            saved_authors.append(author)

        # 创建出版社并保存到数据库
        publishers = [
            models.Publisher(name="人民文学出版社", address="北京市", website="http://rwcn.com", founded_year=1951),
            models.Publisher(name="科幻世界", address="成都市", website="http://sfw.com", founded_year=1979),
            models.Publisher(name="上海译文出版社", address="上海市", website="http://stph.com", founded_year=1978),
        ]
        # 逐个保存出版社以获取ID
        saved_publishers = []
        for publisher in publishers:
            publisher.save()
            saved_publishers.append(publisher)

        # 创建书籍
        books = [
            models.Book(
                title="三体",
                isbn="9787536692930",
                publication_date="2008-01-01",
                price=45.00,
                pages=302,
                genre="SCI",
                author=saved_authors[0],
                publisher=saved_publishers[1]
            ),
            models.Book(
                title="流浪地球",
                isbn="9787221133666",
                publication_date="2016-06-01",
                price=38.00,
                pages=280,
                genre="SCI",
                author=saved_authors[0],
                publisher=saved_publishers[1]
            ),
            models.Book(
                title="活着",
                isbn="9787506365437",
                publication_date="2012-08-01",
                price=28.00,
                pages=191,
                genre="FIC",
                author=saved_authors[1],
                publisher=saved_publishers[0]
            ),
            models.Book(
                title="许三观卖血记",
                isbn="9787506365444",
                publication_date="2014-01-01",
                price=32.00,
                pages=269,
                genre="FIC",
                author=saved_authors[1],
                publisher=saved_publishers[0]
            ),
            models.Book(
                title="红高粱家族",
                isbn="9787530211075",
                publication_date="2017-01-01",
                price=39.80,
                pages=356,
                genre="FIC",
                author=saved_authors[2],
                publisher=saved_publishers[0]
            ),
            models.Book(
                title="白夜行",
                isbn="9787544258609",
                publication_date="2013-01-01",
                price=49.50,
                pages=538,
                genre="MYS",
                author=saved_authors[3],
                publisher=saved_publishers[2]
            ),
        ]
        # 逐个保存书籍
        saved_books = []
        for book in books:
            book.save()
            saved_books.append(book)

        # 创建评论
        reviews = []
        for i, book in enumerate(saved_books):
            for j in range(3):  # 每本书创建3条评论
                review = models.Review(
                    book=book,
                    reviewer_name=f"读者{i}_{j}",
                    rating=(i + j) % 5 + 1,
                    comment=f"这是对《{book.title}》的第{j + 1}条评论，非常精彩！",
                    is_verified=(i + j) % 2 == 0
                )
                reviews.append(review)

        # 使用 bulk_create 保存评论（这里可以使用 bulk_create，因为书籍已经保存）
        models.Review.objects.bulk_create(reviews)

        # 创建书店
        bookstore1 = models.BookStore.objects.create(name="新华书店", location="北京市朝阳区")
        bookstore2 = models.BookStore.objects.create(name="文艺书店", location="上海市黄浦区")

        # 创建库存
        inventories = []
        for i, book in enumerate(saved_books):
            inventory = models.Inventory(
                book=book,
                bookstore=bookstore1 if i % 2 == 0 else bookstore2,
                quantity=i * 10 + 5
            )
            inventories.append(inventory)

        # 使用 bulk_create 保存库存
        models.Inventory.objects.bulk_create(inventories)

        return HttpResponse("数据初始化成功！")

    def get(self, request):

        """
        获取所有书籍及其作者信息，并统计每本书的评论数量。
        """

        # books = models.Book.objects.select_related("author").prefetch_related("reviews")
        # for book in books:
        #     print(book.title, book.author.name)
        #     print("评论数：", book.reviews.count())

        #-----------------------------------------------------------------------------------

        # # 优化后的代码
        # books = models.Book.objects.select_related("author").prefetch_related("reviews")
        # for book in books:
        #     print(book.title, book.author.name)
        #     # 使用 len() 而不是 count() 来避免额外查询
        #     print("评论数：", len(book.reviews.all()))
        # # -----------------------------------------------------------------------------------
        # books = models.Book.objects.select_related("author").annotate(
        #     review_count=Count("reviews")
        # )
        # for book in books:
        #     print(book.title, book.author.name)
        #     print("评论数：", book.review_count)  # 直接使用注解字段



        """
        获取所有书店，包括它们的库存书籍，每本书的作者和出版社信息，以及每本书的前3条评论。
        """
        # prefetch_related("books__author").prefetch_related("books__publisher") 可以写成 Prefetch("books", queryset=models.Book.objects.select_related("author", "publisher"))
        # bookstores = models.BookStore.objects.prefetch_related("books__author").prefetch_related("books__publisher")
        # reviewers = models.Review.objects.select_related("book")
        # for bookstore in bookstores:
        #     print(bookstore.name, ": ")
        #     for book in bookstore.books.all():
        #         print(book.title, book.author.name, book.publisher.name)
        #         reviewer_count = 0
        #         for reviewer in reviewers:
        #             if reviewer.book_id == book.id:
        #                 print(reviewer.reviewer_name, reviewer.comment)
        #                 reviewer_count += 1
        #                 if reviewer_count >= 3:
        #                     break
        #
        #     print()

        # # ------------------------------------------------------------------------------------
        # # 优化后代码
        # # 预取每本书的前3条评论
        # review_prefetch = Prefetch(
        #     "reviews",
        #     queryset=models.Review.objects.all()[:3],
        #     to_attr="top_reviews"
        # )
        #
        # # 一次性预取所有需要的关联数据
        # bookstores = models.BookStore.objects.prefetch_related(
        #     Prefetch(
        #         "books",
        #         queryset=models.Book.objects.select_related("author", "publisher").prefetch_related(review_prefetch)
        #     )
        # )
        #
        # for bookstore in bookstores:
        #     print(bookstore.name, ": ")
        #     for book in bookstore.books.all():
        #         print(book.title, book.author.name, book.publisher.name)
        #         # 直接使用预取的前3条评论
        #         for review in book.top_reviews:
        #             print(review.reviewer_name, review.comment)
        #     print()



        """
        获取所有科幻类书籍，包括作者信息，以及评分4星以上的评论（只预取符合条件的评论）。
        """
        #
        # books = models.Book.objects.filter(genre="SCI").select_related("author").prefetch_related("reviews")
        # for book in books:
        #     print(book.title, book.author.name)
        #     for review in book.reviews.all():
        #         if review.rating >= 4:
        #             print(review.comment)


        # # -----------------------------------------------------------------------------------------------
        # # 优化后代码
        # # 使用条件预取，只获取评分4星以上的评论
        # books = models.Book.objects.filter(genre="SCI").select_related("author").prefetch_related(
        #     Prefetch(
        #         "reviews",
        #         queryset=models.Review.objects.filter(rating__gte=4),
        #         to_attr="high_rated_reviews"  # 使用 to_attr 避免覆盖默认的 reviews 管理器，因为要用到book.reviews.all()
        #     )
        # )
        #
        # for book in books:
        #     print(book.title, book.author.name)
        #     # 直接使用预取的高分评论
        #     for review in book.high_rated_reviews:
        #         print(review.comment)


        """
        获取每个作者的作品数量、平均评分、以及他们最贵书籍的价格。
        """
        #
        # authors = models.Author.objects.prefetch_related("books").prefetch_related("books__reviews")
        #
        # # print(authors)
        # for author in authors:
        #     print(author.name)
        #     count = 0
        #     sum_rating = 0
        #     max_price = 0
        #     for book in author.books.all():
        #         count += 1
        #         for review in book.reviews.all():
        #             sum_rating += review.rating
        #         max_price = max(max_price, book.price)
        #
        #     print(f"书籍数量：{count}, 平均评分: {sum_rating / count}, 最贵的书籍的价格：{max_price}")
        #

        # ##-----------------------------------------------------------------------------------------------
        # # 优化后代码
        # # 使用 annotate 在数据库层面进行聚合计算
        # authors = models.Author.objects.annotate(
        #     book_count=Count("books"),
        #     avg_rating=Avg("books__reviews__rating"),
        #     max_price=Max("books__price")
        # ).prefetch_related("books__reviews")
        #
        # for author in authors:
        #     print(author.name)
        #     print(
        #         f"书籍数量：{author.book_count}, 平均评分: {author.avg_rating or 0}, 最贵的书籍的价格：{author.max_price or 0}")


        #
        # """
        # 获取所有出版社，包括它们出版的书籍，但只包含页数超过300页的书籍，并且预取这些书籍的已验证评论。
        # """
        #
        # publishers = models.Publisher.objects.prefetch_related("books").prefetch_related("books__reviews")
        #
        # for publisher in publishers:
        #     print(publisher.name, ": ")
        #     for book in publisher.books.all():
        #         if book.pages > 300:
        #             print(book.title, ": ", end="")
        #             for review in book.reviews.all():
        #                 if  review.is_verified:
        #                     print(review.comment, end="")
        #             print()
        #


        # # ------------------------------------------------------------------------------------------
        # # 优化后代码
        # # 预取厚书籍及其已验证评论
        # thick_books_with_verified_reviews = Prefetch(
        #     "books",
        #     queryset=models.Book.objects.filter(pages__gt=300).prefetch_related(
        #         Prefetch(
        #             "reviews",
        #             queryset=models.Review.objects.filter(is_verified=True),
        #             to_attr="verified_reviews"
        #         )
        #     )
        # )
        #
        # publishers = models.Publisher.objects.prefetch_related(thick_books_with_verified_reviews)
        #
        # for publisher in publishers:
        #     print(publisher.name, ": ")
        #     for book in publisher.books.all():
        #         print(book.title, ": ", end="")
        #         # 直接使用预取的已验证评论
        #         for review in book.verified_reviews:
        #             print(review.comment, end="")
        #         print()
        #

        #
        # """
        # 获取所有有库存的书店，包括库存书籍的详细信息（作者、出版社），以及这些书籍的平均评分。
        # """
        #
        # inventorys = models.Inventory.objects.filter(quantity__gt=0).prefetch_related("bookstore__books").prefetch_related("book__author").prefetch_related("book__publisher").prefetch_related("book__reviews")
        # # print(inventorys)
        # bookstores = dict()
        # for inventory in inventorys:
        #     sum_rating = 0
        #     count = inventory.book.reviews.count()
        #
        #     for review in inventory.book.reviews.all():
        #         sum_rating += review.rating
        #
        #     bookstore_name = inventory.bookstore.name
        #     bookstores[bookstore_name] = bookstores.get(bookstore_name, [])
        #     ss = (f"书名：{inventory.book.title}, 作者：{inventory.book.author.name}, 出版社：{inventory.book.publisher}"
        #           f"库存：{inventory.quantity}，图书平均评分：{sum_rating / count}")
        #     bookstores[bookstore_name].append(ss)
        #
        #     # print(f"书店：{inventory.bookstore.name} "
        #     #       f"\n\t书名：{inventory.book.title}, 作者：{inventory.book.author.name}, 出版社：{inventory.book.publisher}"
        #     #       f"\n\t库存：{inventory.quantity}，图书平均评分：{sum_rating / count}")
        #
        #
        # # print(bookstores)
        # import json
        # print(json.dumps(bookstores, indent=4, ensure_ascii=False))


        # # ----------------------------------------------------------------------------------------------------------------------
        # # 优化后代码
        #
        # inventories = models.Inventory.objects.filter(
        #     quantity__gt=0
        # ).select_related(
        #     'bookstore', 'book', 'book__author', 'book__publisher'
        # ).annotate(
        #     book_avg_rating=Avg('book__reviews__rating')
        # )
        #
        # result = {}
        # for inventory in inventories:
        #     bookstore_name = inventory.bookstore.name
        #     if bookstore_name not in result:
        #         result[bookstore_name] = []
        #
        #     book_info = (
        #         f"书名：{inventory.book.title}, "
        #         f"作者：{inventory.book.author.name}, "
        #         f"出版社：{inventory.book.publisher.name}, "
        #         f"库存：{inventory.quantity}，"
        #         f"图书平均评分：{inventory.book_avg_rating or 0:.2f}"
        #     )
        #     result[bookstore_name].append(book_info)
        #
        # import json
        # print(json.dumps(result, indent=4, ensure_ascii=False))
        #
        #
        #


        return HttpResponse("get ok")




class ModelDemoView(View):
    def get(self, request):

        # md = models.ModelDemo.objects.all()
        # print(md)
        # # 查找成年人，年龄大于等于18岁
        # md = models.ModelDemo.objects.filter(age__gte=18)
        # print(md)

        # # 不推荐使用这种方式，因为代码结构不规范了，查询数据库操作的时候一般都要使用objects
        # md = models.ModelDemo.get_access_user()
        # print(md)

        """当需要给模型扩展一些数据操作方法或者属性时，可以使用自定义模型模型管理器或者代理模型"""

        md = models.ModelDemo.objects.get_access_user()
        print(md) # <QuerySet [<ModelDemo: 李四>, <ModelDemo: 赵六>, <ModelDemo: 钱七>]>


        female = models.FemaleUser.all()
        print(female)
        male = models.MaleUser.all()
        print(male)
        return HttpResponse("model demo view get ok")