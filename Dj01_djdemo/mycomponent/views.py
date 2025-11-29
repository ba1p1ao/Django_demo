from django.core.signals import request_started
from django.shortcuts import render
from django.views import View
from django.http import HttpRequest, HttpResponse, JsonResponse
from mycomponent import models
from student import models
from django.contrib import staticfiles
import orjson
import os

class SoftwareView(View):
    def get(self, request: HttpRequest):

        return render(request, "component/software_index.html", locals())

    def post(self, request: HttpRequest):
        print(request.POST)

        software_data = {
            "name": request.POST.get("name"),
            "version": request.POST.get("version"),
            "website": request.POST.get("website"),
            "picture": request.FILES.get("picture"),
            "downloads": request.FILES.get("downloads"),
        }

        software_obj = models.Software.objects.create(**software_data)
        print(software_obj)
        # print(software_data)
        return JsonResponse({})

    def delete(self, request: HttpRequest):
        print(models.Software.objects.all())
        request_data = orjson.loads(request.body)
        id = request_data.get("id")
        software = models.Software.objects.get(id=id)
        # print(software)
        if software:
            soft_downloads_path = software.downloads.path
            soft_picture_path = software.picture.path
            if os.path.exists(soft_downloads_path):
                os.remove(soft_downloads_path)
            if os.path.exists(soft_picture_path):
                os.remove(soft_picture_path)
            software.delete()

        print(models.Software.objects.all())
        return HttpResponse("delete ok")




from django.core.paginator import Paginator
class PageView(View):
    def get(self, request: HttpRequest):

        """数据分页"""
        """提供了数据对象列表以及单页数据量，创建分页器对象"""
        students = models.Student.objects.all()
        paginator = Paginator(list(students), 10)
        # print(paginator)
        # print(students)
        # 总数据量
        # print("总数据量：", paginator.count)
        # # 每一页有多少数据
        # print("每一页有多少数据：", paginator.per_page)
        # # 能分多少页
        # print("能分多少页：", paginator.num_pages)
        # # 页码列表
        # print("页码列表：", paginator.page_range)

        """基于分页器对象，创建分页对象"""
        # 接受客户端的页码，页面一般都是查询字符串，或者路径参数
        current_page = request.GET.get("page", 1)
        page = paginator.page(current_page)
        # # 当前页要展示给外界的数据对象列表
        # print(page.object_list)
        # # 当前页码
        # print(page.number)
        # # 逆向查找当前Page分页对象的父级分页器对象
        # print(page.paginator)

        return render(request, "component/page_index.html", locals())


    # """不使用 Paginator，实现分类功能"""
    # def get(self, request: HttpRequest):
    #     current_page = int(request.GET.get("page", 1))
    #     page_nums = 10
    #     students = models.Student.objects.all()[current_page:page_nums]
    #     print(students)
    #
    #     return render(request, "component/page_index.html", locals())



from django.views.decorators.cache import cache_page
from django.core.cache import cache


# 一为了避免所有视图缓存同一时间过期，造成服务器需要在短时间内生成大量的缓存，一般是设置随机数过期时间。
@cache_page(timeout=100)
def funccache(request):

    print("开始缓存")
    return HttpResponse("func cache ok")


# 如果使用类视图，cache_page 这个装饰器返回的是一个函数，只适用于函数视图，所以需要django的工具里面的method_decorator进行类视图转换
# cache_page 是基于函数视图进行缓存的，所以无法直接给类视图使用，需要使用method_decorator进行类视图转换
from django.utils.decorators import method_decorator
class CacheView(View):
    # method_decorator的使用方法
    @method_decorator(cache_page(timeout=100))
    def get(self, request):
        # 获取 student 的数据
        models_students = list(models.Student.objects.values_list())
        print(type(models_students))
        # print(models_students)
        print("method 开始缓存")
        return JsonResponse(models_students, safe=False)



"""
缓存API
是针对于某个变量数据进行单独缓存的，使用上比视图缓存更为灵活。

设置：cache.set(键,值,有效时间)
获取：cache.get(键)
删除：cache.delete(键)
清空：cache.clear() # 慎用，这个会把整个库所有的 缓存数据全部清空！
"""

# 导入cache 方法

# caches 如果 在settings.py中配置多个Redis连接，在代码中通过caches['name']指定使用
from django.core.cache import cache, caches


class APICacheView(View):
    def get(self, request):
        current_cache = caches["default"]
        print(current_cache)
        models_students = cache.get("models_students")
        if not models_students:
            print("设置 cache")
            models_students = list(models.Student.objects.values_list())
            cache.set("models_students", models_students, timeout=30)

        return JsonResponse(models_students, safe=False)


    def delete(self, request):
        """更新或者删除"""

        # 删除/更新数据时，先删缓存，再删除/更新数据库的数据
        cache.delete("student_list")
        # 删除/更新数据库的数据 代码

        return JsonResponse({}, safe=False)


"""
缓存适用于哪些场景？不适用于哪些场景？
适用于数据稳定，不会经常发生变化的业务中，例如：配置信息，文章、新闻、商品等展示数据。
不适用于实时性要求比较高的业务中，例如：股市k线图，实时直播的新闻、聊天....
"""