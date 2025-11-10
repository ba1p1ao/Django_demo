## 第一个django项目

### 创建django项目
```bash
# 项目名称与函数变量名命名方式一样

django-admin startproject Dj01_djdemo
```

### 启动服务

```bash
python manager.py runsever 8000
```

### 创建子服务
```bash
python manage.py startapp goods
```

### 编写good/view 视图函数

```python

from django.shortcuts import render
from django.http.response import HttpResponse

# Create your views here.

def index(request):
    data = "<h1>hello world</h1>"
    return HttpResponse(data, content_type="text/html")

```

### 编写路由
```python
# 再主项目里面的urls.py

from django.contrib import admin
from django.urls import path
from goods import views as goodsViews

urlpatterns = [
    path('admin/', admin.site.urls),
    path("index/", goodsViews.index, name="goods") # 添加自己项目的视图函数位置
]
```