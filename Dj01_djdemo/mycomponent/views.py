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

