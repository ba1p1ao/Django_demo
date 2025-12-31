from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import authentication_classes, permission_classes
from exam_system.settings import JWT_EXPIRE_TIME
from apps.user.models import User
from apps.user.serializers import UserSerializers, UserUpdateSerializer
from utils.ResponseMessage import MyResponse
from utils.PasswordEncode import verify_password, hash_password
from utils.JWTAuth import create_token


class UserLoginView(APIView):
    # 登录接口不需要认证
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        if not username or not password:
            return MyResponse.failed("用户名和密码不能为空")

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return MyResponse.failed("用户名或密码错误")

        if not verify_password(password, user.password):
            return MyResponse.failed("用户名或密码错误")

        user_info = UserSerializers(instance=user).data
        token = create_token(payload=user_info, timeout=JWT_EXPIRE_TIME)

        return MyResponse.success(message="登录成功", data={
            'token': token,
            'user_info': user_info
        })



class UserInfoView(APIView):
    def get(self, request):
        payload = request.user
        if not payload:
            return MyResponse.other(code=403, message="用户信息已过期，请重新登录")

        username = payload.get("username")
        if not username:
            return MyResponse.other(code=403, message="用户信息已过期，请重新登录")

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return MyResponse.failed(message="用户不存在")

        userinfo = UserSerializers(instance=user).data
        return MyResponse.success(data=userinfo)



class UserRegisterView(APIView):

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        nickname = request.data.get('nickname')
        role = request.data.get('role')

        # 验证必填字段
        if not all([username, password, nickname, role]):
            return MyResponse.failed("用户名、密码、昵称和角色不能为空")

        # 验证角色
        if role not in ['student', 'teacher']:
            return MyResponse.failed("角色只能是student或teacher")

        # 检查用户名是否已存在
        if User.objects.filter(username=username).exists():
            return MyResponse.failed("该用户已存在")

        user_serializer = UserSerializers(data=request.data)

        if user_serializer.is_valid():
            user_serializer.save()
            return MyResponse.success(message="注册成功", data={"id": user_serializer.data.get("id")})

        return MyResponse.failed(message="注册失败", data=user_serializer.errors)



class UserUpdateView(APIView):
    def put(self, request):

        payload = request.user
        if not payload:
            return MyResponse.other(code=403, message="用户信息已过期，请重新登录")

        user_id = payload.get("id")
        if not user_id:
            return MyResponse.other(code=403, message="用户信息已过期，请重新登录")

        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return MyResponse.failed(message="用户不存在")

        user_ser = UserUpdateSerializer(instance=user, data=request.data, partial=True)
        if user_ser.is_valid():
            user_ser.save()
            return MyResponse.success(message="更新成功")

        return MyResponse.failed(message="更新失败", data=user_ser.errors)



class UserPasswordView(APIView):
    def put(self, request):

        payload = request.user
        if not payload:
            return MyResponse.other(code=403, message="用户信息已过期，请重新登录")

        user_id = payload.get("id")
        if not user_id:
            return MyResponse.other(code=403, message="用户信息已过期，请重新登录")

        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return MyResponse.failed(message="用户不存在")

        old_password = request.data.get("old_password")
        new_password = request.data.get("new_password")

        # 验证必填字段
        if not old_password or not new_password:
            return MyResponse.failed("原密码和新密码不能为空")

        # 验证原密码
        if not verify_password(old_password, user.password):
            return MyResponse.failed(message="原密码不正确")

        # 更新密码
        user.password = hash_password(new_password)
        user.save()

        return MyResponse.success(message="密码修改成功")

