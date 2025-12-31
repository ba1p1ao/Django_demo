from rest_framework.views import APIView
from utils.CaptchaCode import get_digits
from utils.PasswordEncode import get_md5
from utils.ResponseMessage import ToolsResponse
from django.core.cache import cache, caches

class CaptchaCodeAPIView(APIView):
    def get(self, request):
        try:
            captcha_uuid, captcha_md5, base64_image = get_digits(4)
            # 使用 UUID 作为键，MD5 加密的验证码作为值
            cache.set(captcha_uuid, captcha_md5, timeout=180)
            response_data = {
                "uuid": captcha_uuid,
                "image": base64_image,
                "message": "验证码生成成功",
                "expire_time": 180  # 过期时间（秒）
            }
            print(response_data)
            return ToolsResponse.success(response_data)
        except Exception as e:
            # 处理异常
            return ToolsResponse.failed(f"验证码生成失败: {str(e)}")


class CaptchaVerifyAPIView(APIView):
    def post(self, request):
        uuid = request.data.get("captcha_id")
        code = request.data.get("captcha_text")

        if not uuid or not code:
            return ToolsResponse.failed("请重新输入验证码")

        verufy_code = cache.get(uuid)
        if not verufy_code:
            return ToolsResponse.failed("验证码已过期，请重新获取")

        user_code_md5 = get_md5(code)
        if user_code_md5 == verufy_code:
            cache.delete(uuid)
            return ToolsResponse.success("验证码正确")
        else:
            return ToolsResponse.failed("验证码错误，请重新输入")
