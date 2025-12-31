from rest_framework.generics import GenericAPIView
from rest_framework.views import APIView
from apps.user.serializers import UserSerializer
from apps.user import models
from utils.ResponseMessage import UserResponse
from utils.PasswordEncode import verify_password, hash_password
from utils.JWTAuth import create_token, get_payload
from datetime import datetime
from django.utils import timezone
from muxishop.settings import JWT_EXPIRE_TIME

class UserExistAPIView(APIView):
    def post(self, request):
        email = request.data.get("email")
        if models.User.objects.filter(email=email):
            return UserResponse.failed("该用户已经存在")
        return UserResponse.success("")



class UserRegisterAPIView(APIView):

    def post(self, request):
        # 反序列化，将 json 转 obj ， rest_framework APIView 已经帮我们将 request.body 转成了 json
        user_serializer = UserSerializer(data=request.data)
        # 验证数据的合法性, 验证 UserSerializer 里面的规则
        # 需要添加 raise_exception=True 如果数据不合法，抛出异常
        try:
            if user_serializer.is_valid(raise_exception=True):
                user_data = user_serializer.save()
                # 序列化 obj 转 json
                user_json = UserSerializer(instance=user_data).data
                return UserResponse.success(user_json, safe=False)
        except Exception as e:
            return UserResponse.failed(f"所填信息有误 {e}", safe=False)
        return UserResponse.failed("用户添加失败", safe=False)

    def get(self, request):
        email = request.GET.get("email")
        if not email:
            return UserResponse.failed("邮箱信息不存在", safe=False)
        try:
            user = models.User.objects.get(email=email)
            # 反序列化 obj 转 json
            user_json = UserSerializer(instance=user).data
            return UserResponse.success(user_json, safe=False)
        except Exception as e:
            return UserResponse.failed("用户信息不存在", safe=False)


class UserLoginView(GenericAPIView):
    def post(self, request):
        email = request.data.get("username")
        password = request.data.get("password")
        # print(email, password)
        try:
            user = models.User.objects.get(email=email)
        except Exception as e:
            return UserResponse.other("用户名或密码错误", safe=False)

        if not verify_password(password, user.password):
            return UserResponse.other("用户名或密码错误", safe=False)
        payload = UserSerializer(instance=user).data
        token = create_token(payload=payload, timeout=JWT_EXPIRE_TIME)
        response_data = {
            "username": user.name,
            "email": email,
            "token": token,
        }
        return UserResponse.success(response_data, safe=False)


class UserInfoAPIView(APIView):
    def get(self, request):
        if not request.user.get("status"):
            return UserResponse.failed("用户信息已过期，请重新登录", safe=False)

        email = request.user.get("payload").get("email")
        try:
            user = models.User.objects.get(email=email)
        except Exception as e:
            return UserResponse.failed("用户信息不存在，请重新登录", safe=False)

        response_data = UserSerializer(instance=user).data
        print(response_data)
        return UserResponse.success(response_data)

    def post(self, request):
        if not request.user.get("status"):
            return UserResponse.failed("用户信息已过期，请重新登录", safe=False)
        email = request.user.get("payload").get("email")
        user = models.User.objects.filter(email=email)
        if not user:
            return UserResponse.failed("用户信息不存在，请重新登录", safe=False)
        request_data = request.data
        if email != request_data["email"] and models.User.objects.filter(email=request_data["email"]).first():
            return UserResponse.failed("邮箱已经存在", safe=False)
        print(request_data)
        request_data["birthday"] = timezone.make_aware(datetime.strptime(request_data["birthday"], "%Y-%m-%d"))
        # print(request_data)
        try:
            user.update(**request_data)
            return UserResponse.success("修改成功")
        except Exception as e:
            print(e)
            return UserResponse.failed("修改失败")




class UpdateUserPasswordAPIView(APIView):
    def post(self, request):
        print("password     ", request.user)
        if not request.user.get("status"):
            return UserResponse.failed("用户信息已过期，请重新登录", safe=False)
        email = request.user.get("payload").get("email")
        user = models.User.objects.filter(email=email).first()
        if not user:
            return UserResponse.failed("用户信息不存在，请重新注册", safe=False)
        print(request.data)
        oldpassword = request.data.get("oldpassword")
        if not verify_password(oldpassword, user.password):
            return UserResponse.failed("原密码错误，请重新输入", safe=False)

        password = request.data.get("password")
        updated_count = models.User.objects.filter(email=email).update(password=hash_password(password))

        if updated_count == 0:
            return UserResponse.failed("密码修改失败", safe=False)

        return UserResponse.success("修改成功")