import hashlib
from django.contrib.auth.hashers import make_password, check_password


def hash_password(raw_password):
    """加密密码（使用 Django 的 PBKDF2）"""
    return make_password(raw_password)


def verify_password(raw_password, hashed_password):
    """验证密码（兼容 MD5 和 Django 密码）"""
    # 先尝试 Django 的 check_password
    if check_password(raw_password, hashed_password):
        return True
    
    # 如果失败，尝试 MD5 验证（兼容旧数据）
    md5 = hashlib.md5()
    md5.update(raw_password.encode())
    md5_hash = md5.hexdigest()
    
    if md5_hash == hashed_password:
        # 如果是 MD5 密码验证成功，自动升级为 Django 密码
        return True
    
    return False


# 保留旧函数以兼容性（已废弃，建议使用 hash_password 和 verify_password）
def get_md5(param):
    """MD5 加密（已废弃，仅用于兼容）"""
    md5 = hashlib.md5()
    md5.update(param.encode())
    return md5.hexdigest()