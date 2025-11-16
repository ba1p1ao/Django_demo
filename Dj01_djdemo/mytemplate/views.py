from django.shortcuts import render # render 用于渲染template模版页面
from django.http import HttpRequest, HttpResponse


# Create your views here.

def index(request: HttpRequest):
    # name = "hello dtl"
    # return render(request, "index.html", locals())

    # 模拟页面读取静态页面
    # 如果缓存中存在静态页面，直接显示，如果不存在生成后显示
    import os
    from Dj01_djdemo.settings import BASE_DIR
    from django.template import loader

    data = {
        "name": "hello dtl"
    }
    static_html_filename = 'index.html'
    static_html_path = BASE_DIR / "cache" / static_html_filename
    if os.path.exists(static_html_path):
        # 读取缓存文件
        print("读取缓存文件")
        with open(static_html_path, 'rb') as f:
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
        with open(static_html_path, 'w') as f:
            f.write(content)

    return HttpResponse(content)

