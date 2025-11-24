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


## 路由分层

- 主要解决了多个子应用混在一起的情况
- 可以通过路由控制某一个应用

### 具体使用
1. 创建两个应用 goods ， users
``` bash
python manager.py startapp goods
python manager.py startapp users
```

2. 编写各自的 views
``` python
## goods/views.py
@require_http_methods(["POST"]) # 注意，中括号中的请求方法名务必大写!!!否则无法正常显示
def index(request):
    data = "<h1>hello goods/index</h1>"
    return HttpResponse(data, content_type="text/html")



@require_http_methods(["GET"]) 
def goods(request):
    data = "<h1>hello goods/goods</h1>"
    return HttpResponse(data, content_type="text/html")



## users/views.py
@require_http_methods(["POST"])  # 注意，中括号中的请求方法名务必大写!!!否则无法正常显示
def index(request):
    data = "<h1>hello user/index</h1>"
    return HttpResponse(data, content_type="text/html")


@require_http_methods(["GET"])
def users(request):
    data = "<h1>hello user/users</h1>"
    return HttpResponse(data, content_type="text/html")

```

3. 如果再主项目的urls导入这两个应用的views，就会出现重名的现象，为了避免重名 需要使用 as 所以，采用路由分层的方式
- 创建goods/urls.py, 后添加有关goods的views函数
``` python
from django.urls import path
from goods import views

# goods/urls.py, 为子路由
urlpatterns = [
    path("goods/", view=views.goods),
    path("index/", view=views.index),
]
```
- 创建users/urls.py, 后添加有关users的views函数
``` python
from django.urls import path
from users import views

urlpatterns = [
    path("index/", views.index),
    path("users/", views.users),
]
```
- 最后修改主项目的urls
``` python
from django.contrib import admin
from django.urls import path, include

# 路由分层
# 主项目的urls为主路由，include可以添加子路由
urlpatterns = [
    path("admin/", admin.site.urls),
    path("goods/", include("goods.urls")), # 添加前缀， localhost:8000/goods/ + goods 的路由
    path("users/", include("users.urls")),
]

```
5. 当django项目中的路由分层以后，视图的访问地址就分成2段组合:总路由和子应用路由。那么用户访问视图,则访问url地址的规则:
- 想要请求goods的index视图函数，就要访问http://localhost:8000/goods/goods



6. 开启数据库查询日志

```sql
show variables like "%general_log%";

+------------------+---------------------------------+
| Variable_name    | Value                           |
+------------------+---------------------------------+
| general_log      | OFF                             |
| general_log_file | /var/lib/mysql/ff969a281c3a.log |
+------------------+---------------------------------+

set global general_log = 'ON';
```
```bash
tail -f /var/lib/mysql/ff969a281c3a.log
```