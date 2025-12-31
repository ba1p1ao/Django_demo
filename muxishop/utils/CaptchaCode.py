import base64
import random
import string
import uuid
from io import BytesIO
from captcha.image import ImageCaptcha
from utils.PasswordEncode import verify_password, get_md5


def generate_captcha_text(length=4, use_digits=True, use_letters=True):
    """生成验证码文本"""
    if use_digits and use_letters:
        # 字母+数字，移除容易混淆的字符
        confusing_chars = '0oO1ilI'
        chars = string.ascii_letters + string.digits
        chars = ''.join([c for c in chars if c not in confusing_chars])
    elif use_digits:
        # 仅数字
        chars = string.digits
    else:
        # 仅字母
        chars = string.ascii_letters

    # 生成验证码文本
    return ''.join(random.choices(chars, k=length))


def get_captcha(captcha_type='digits', length=4):
    """
    生成验证码的通用函数

    Args:
        captcha_type: 'digits'数字, 'letters'字母, 'mixed'混合
        length: 验证码长度

    Returns:
        tuple: (uuid, md5加密的验证码, base64图片数据)
    """
    # 1. 生成验证码文本
    if captcha_type == 'digits':
        text = generate_captcha_text(length, use_digits=True, use_letters=False)
    elif captcha_type == 'letters':
        text = generate_captcha_text(length, use_digits=False, use_letters=True)
    else:  # 'mixed'
        text = generate_captcha_text(length, use_digits=True, use_letters=True)

    # 2. 生成验证码图片
    image = ImageCaptcha().generate_image(text)

    # 3. 转换为base64
    buffer = BytesIO()
    image.save(buffer, format='PNG', optimize=True)
    buffer.seek(0)

    img_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')

    # 4. 清理内存
    buffer.close()
    del image, buffer

    # 5. 返回结果
    return (
        str(uuid.uuid4()),  # uuid
        get_md5(text),  # md5加密的验证码
        f"data:image/png;base64,{img_base64}"  # base64图片
    )


# 保持原有接口的兼容性
def get_digits(length=4):
    return get_captcha('digits', length)


def get_letters(length=4):
    return get_captcha('letters', length)


def get_letters_digits(length=4):
    return get_captcha('mixed', length)


# 使用示例
if __name__ == '__main__':
    # 生成数字验证码
    uuid_str, md5_str, base64_img = get_digits(4)
    print(f"UUID: {uuid_str}")
    print(f"MD5: {md5_str}")
    print(f"图片Base64前50位: {base64_img[:50]}...")

    # 或者直接使用通用函数
    result = get_captcha('mixed', 6)
    print(f"\n混合验证码UUID: {result[0]}")