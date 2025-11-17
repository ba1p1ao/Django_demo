from django.shortcuts import render  # render 用于渲染template模版页面
from django.http import HttpRequest, HttpResponse
from django.conf import settings
import time
from datetime import datetime
# Create your views here.


def index(request: HttpRequest):
    # name = "hello dtl"
    # return render(request, "index.html", locals())

    # 模拟页面读取静态页面
    # 如果缓存中存在静态页面，直接显示，如果不存在生成后显示
    import os
    from Dj01_djdemo.settings import BASE_DIR
    from django.template import loader

    data = {"name": "hello dtl"}
    static_html_filename = "index.html"
    static_html_path = BASE_DIR / "cache" / static_html_filename
    if os.path.exists(static_html_path):
        # 读取缓存文件
        print("读取缓存文件")
        with open(static_html_path, "rb") as f:
            content = f.read()
    else:
        # # 加载模板文件
        # template = loader.get_template(static_html_filename)
        # # 渲染模板文件
        # content = template.render(data, request)

        # 加载模板文件并渲染
        content = loader.render_to_string(static_html_filename, data, request)
        # 写入缓存文件
        print("写入缓存文件")
        with open(static_html_path, "w") as f:
            f.write(content)

    return HttpResponse(content)


def get_template(request: HttpRequest):


    num1 = 100
    num2 = 3.14
    name = "lihua"
    data1 = {1, 2, 3}
    data2 = (1, 2, 3, 4)
    data3 = [1, 2, 3, 4]
    data4 = {"name": "lihua", "age": 17}
    setting = settings
    book_list = [
        {
            "id": 10,
            "price": 9.90,
            "name": "python3天入门到挣扎",
        },
        {
            "id": 11,
            "price": 19.90,
            "name": "python7天入门到垂死挣扎",
        },
    ]
    time1 = time
    return render(request, "template.html", locals())



def iffor(request: HttpRequest):
    name = "root"

    """标签[循环]"""
    book_list1 = [
        {"id": 11, "name": "python基础入门", "price": 130.00},
        {"id": 17, "name": "Go基础入门", "price": 230.00},
        {"id": 23,"name": "PHP基础入门", "price": 330.00},
        {"id": 44, "name": "Java基础入门", "price": 730.00},
        {"id": 51, "name": "C++基础入门", "price": 300.00},
        {"id": 56, "name": "C#基础入门", "price": 100.00},
        {"id": 57, "name": "前段基础入门", "price": 380.00},
    ]

    return render(request, "iffor.html", locals())


def myfilter(request: HttpRequest):
    """过滤器"""
    title = "我的标题"
    content = '我的个人主页：<a href="http://www.baidu.com">点击查看</a>'
    time1 = datetime.now()
    file_size = 2342512
    address = ["中国", "北京", "海淀"]
    mobile = "13412341234"

    users = [
        {"name": "lihua", "sex": 0, "zichan": 122.08},
        {"name": "liubei", "sex": 1, "zichan": 1432.30},
        {"name": "guanyu", "sex": 1, "zichan": 142.38},
        {"name": "zhangfei", "sex": 1, "zichan": 132.30},
        {"name": "zhaoyun", "sex": 1, "zichan": 112.00},
    ]
    return render(request, "myfilter.html", locals())


def tem_fenli(request: HttpRequest):
    """模板分离技术"""
    return render(request, "tem_fenli.html", locals())


def tem_jicheng_users(request: HttpRequest):
    """模板继承技术"""
    return render(request, "tem_jicheng_users.html", locals())

def tem_jicheng_goods(request: HttpRequest):
    """模板继承技术"""
    return render(request, "tem_jicheng_goods.html", locals())

def tem_jicheng_info(request: HttpRequest):
    return render(request, "tem_jicheng_info.html", locals())
