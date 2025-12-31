import jwt
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed

from exam_system.settings import SECRET_KEY
from django.utils import timezone


def create_token(payload: dict, timeout=3600):
    header = {
        "alg": "HS256",
        "typ": "JWT"
    }
    payload["exp"] = timezone.now() + timezone.timedelta(seconds=timeout)

    return jwt.encode(headers=header, payload=payload, key=SECRET_KEY, algorithm="HS256")


def get_payload(token):
    """解码并验证JWT Token"""
    result = {"status": False, "payload": None, "error": None}
    try:
        result["payload"] = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=["HS256"],
            options={"verify_exp": True}  # 确保验证过期时间
        )
        result["status"] = True
    except jwt.ExpiredSignatureError:
        result["error"] = "Token已过期"
    except jwt.InvalidTokenError as e:
        result["error"] = f"无效Token: {e}"
    return result



class JWTHeaderQueryParamAuthentication(BaseAuthentication):
    """从请求头或查询参数中获取JWT Token进行认证"""
    def authenticate(self, request):
        # 从请求头获取token
        auth_header = request.META.get('HTTP_AUTHORIZATION', '')
        if auth_header:
            # 处理Bearer token格式
            parts = auth_header.split()
            if len(parts) != 2 or parts[0].lower() != 'bearer':
                raise AuthenticationFailed('Token格式错误，应为: Bearer <token>')
            token = parts[1]
        else:
            # 如果请求头中没有，尝试从查询参数获取
            token = request.GET.get("token", "")
            if not token:
                # 如果没有token，返回None让其他认证类处理
                return None

        try:
            # 验证token
            result = get_payload(token)

            # 原代码：返回整个result字典（包含status、payload、error）
            # return (result, token)

            # 新代码：只返回payload作为user对象，符合DRF标准
            if not result.get("status"):
                raise AuthenticationFailed(result.get("error", "Token验证失败"))
            return (result.get("payload"), token)

        except AuthenticationFailed as e:
            raise e

    def authenticate_header(self, request):
        return 'Bearer'