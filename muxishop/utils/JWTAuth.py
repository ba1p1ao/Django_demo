import jwt
from rest_framework.authentication import BaseAuthentication
# 导入 django 提供的加密key
from muxishop.settings import SECRET_KEY
from django.utils import timezone


def create_token(payload: dict, timeout=60):
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

class JWTQueryParamAuthentication(BaseAuthentication):
    def authenticate(self, request):
        url_token = request.GET.get("token")
        result = get_payload(url_token)
        return result, url_token

class JWTHeaderQueryParamAuthentication(BaseAuthentication):
    def authenticate(self, request):
        header_token = request.META.get("HTTP_TOKEN")
        result = get_payload(header_token)
        return result, header_token


if __name__ == '__main__':
    # token = create_token()
    # print(token)
    token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6ImFzZGYiLCJleHAiOjE3NjQ4NDMzNDh9.SkGc44DtlXsSwpCSACfJx1KCfnP0KgbAb6I8X1-f37M'
    print(get_payload(token))
