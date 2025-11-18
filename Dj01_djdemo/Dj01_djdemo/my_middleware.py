from django.http import HttpRequest


# 函数中间件
def simple_middleware(get_response):
    """
    自定义中间件
    param: get_response 相当于是视图函数
    """

    def middleware(request: HttpRequest):
        # 记录访问用户记录的信息,识别判断黑名单,白名单,判断用户是否登录, 判断用户是否拥有访问权限.....
        # 获取 request.header
        print(request.headers)
        # 获取 元数据信息
        print(request.META)
        print("--------------视图执行之前---------------")

        # 执行视图
        response = get_response(request)

        # 记录用户的操作历史,访问历史,日志记录, 资源的回收...
        # 获取用户访问的路径
        print(request.META.get("REMOTE_ADDR"), request.META.get("PATH_INFO"))
        print("--------------视图执行之后---------------")

        # 返回视图函数执行后的结果
        return response

    return middleware


# 类中间件
# class SimpleMiddleware:
#     def __init__(self, get_response):
#         self.get_response = get_response
#
#     def __call__(self, request: HttpRequest, *args, **kwargs):
#         print("--------------类中间件视图执行之前---------------")
#         response = self.get_response(request)
#         print("--------------类中间件视图执行之后---------------")
#         return response


# 类中间件继承MiddlewareMixin
from django.utils.deprecation import MiddlewareMixin  # Mixin 表示当前类是一个混入类，扩展类，混入类的作用就是保存一些类的公共方法
from django.http import HttpResponse, HttpRequest


# 类中间件中提供了5个基本钩子方法，方法名是固定的，
# 一旦实现了这些方法，会在请求与响应过程中按指定的顺序分别执行。
class SimpleMiddleware(MiddlewareMixin):
    def process_request(self, request: HttpRequest):
        """
        方法名是固定的,该方法会在用户请求访问路由解析完成以后,调用视图之前自动执行
        不需要返回值

        用途：权限,路由分发,cdn,用户身份识别,白名单,黑名单..
        注意：此方法不能使用return,使用则报错!!!
        """
        print("-------------- 1. 视图执行之前，会自动执行 process_request ---------------")
        # 获取request中的数据
        # 获取 request.header
        # print(request.headers)
        # 获取 元数据信息
        # print(request.META)
        print(request.session.__dict__)

    def process_view(self, request: HttpRequest, view_func, view_args, view_kwargs):
        """
        用途:进行缓存处理,识别参数,根据参数查询是否建立缓存
        """
        print("-------------- 2. 视图接受参数之后，视图执行之前，会自动执行 process_view ---------------")
        # 判断请求信息时候再缓存中，直接返回
        # 如果直接返回response对象，就不会执行视图的内容
        # 做到如果缓存中存在想要请求的数据，直接返回，不会调用数据库
        # print(locals())

    def process_response(self, request: HttpRequest, response):
        """
        必须有返回值，否则报错
        """
        print("-------------- 5. 视图执行之后，会自动执行 process_response ---------------")
        # 记录用户的操作历史,访问历史,日志记录, 资源的回收...
        # 获取用户访问的路径
        print(request.META.get("REMOTE_ADDR"), request.META.get("PATH_INFO"))
        return response

    def process_exception(self, request: HttpRequest, exception):
        """
        当视图引发异常时，Django 会调用 process_exception()。process_exception() 应该返回 None 或 HttpResponse 对象
        """
        print("-------------- 4. 视图执行中，如果报错，会自动执行 process_exception ---------------")
        print(exception)

    def process_template_response(self, request, response):
        """
        用途:建立静态化HTML页面缓存
        process_template_response() 在视图被完全执行后调用，如果响应实例有 render() 方法，表明它是一个 TemplateResponse 或等效对象。
        """
        print("-------------- 4. 视图执行过程中，如果视图调用了template模板，就会自动执行 process_template_response ---------------")
        print(f"Template name: {response.template_name}")

        # 必须返回响应对象
        return response