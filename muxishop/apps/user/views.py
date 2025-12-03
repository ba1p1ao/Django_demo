from rest_framework.views import APIView
from apps.user.serializers import UserSerializer
from apps.user import models
from utils.ResponseMessage import UserResponse


class UserRegisterAPIView(APIView):

    def post(self, request):
        # 反序列化，将 json 转 obj ， rest_framework APIView 已经帮我们将 request.body 转成了 json
        user_serializer = UserSerializer(data=request.data)
        # 验证数据的合法性, 验证 UserSerializer 里面的规则
        # 需要添加 raise_exception=True 如果数据不合法，抛出异常
        if user_serializer.is_valid(raise_exception=True):
            user_data = user_serializer.save()
            # 序列化 obj 转 json
            user_json = UserSerializer(instance=user_data).data
            return UserResponse.success(user_json, safe=False)

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
