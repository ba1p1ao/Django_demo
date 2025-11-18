from django.shortcuts import render
from django.views import View
from django.http import HttpResponse, HttpRequest


# Create your views here.

# class UserView(View):
#     def get(self, request: HttpRequest):
#         return HttpResponse("user get")
#
#     def post(self, request: HttpRequest):
#         return HttpResponse("user post")
#
#     def delete(self, reuqest: HttpRequest):
#         return HttpResponse("User delete")
#
#     def put(self, request: HttpRequest):
#         return HttpResponse("User put")


### 如果 user 视图存在多个get请求，采用多个类的方式

# 用户列表视图
class UserListView(View):
    def get(self, request: HttpRequest):
        print("-------------- 3. 视图已经执行 ---------------")
        print(request.GET)
        return HttpResponse(f"Get user list data={request.GET}")

    def post(self, request: HttpRequest):
        print(request.POST)
        return HttpResponse(f"Create new user data={request.POST}")


# 用户详情视图
class UserDetailView(View):
    def get(self, request, user_id):
        return HttpResponse(f"Get user by ID: {user_id}")

    def put(self, request, user_id):
        return HttpResponse(f"Update user: {user_id}")

    def delete(self, request, user_id):
        return HttpResponse(f"Delete user: {user_id}")


# 根据姓名查询用户的视图
class UserByNameView(View):
    def get(self, request, name):
        return HttpResponse(f"Get user by name: {name}")
