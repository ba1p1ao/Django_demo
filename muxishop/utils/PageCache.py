"""
页面缓存工具类
用于缓存用户访问的页面数据，减少数据库查询，提升性能
"""

from django.core.cache import cache
from functools import wraps
import hashlib
import json


def page_cache(timeout=300, key_prefix="page", user_aware=False):
    """
    页面缓存装饰器
    
    Args:
        timeout: 缓存过期时间（秒），默认 5 分钟
        key_prefix: 缓存键前缀
        user_aware: 是否区分用户，True 时不同用户的缓存独立
    
    Usage:
        @page_cache(timeout=600, key_prefix="goods_list")
        def get_goods_list(request):
            ...
    
        @page_cache(timeout=300, user_aware=True)
        def get_user_cart(request):
            ...
    """
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            # 生成缓存键
            cache_key = _generate_cache_key(
                request, 
                key_prefix, 
                user_aware, 
                *args, 
                **kwargs
            )
            
            # 尝试从缓存获取数据
            cached_data = cache.get(cache_key)
            if cached_data is not None:
                return cached_data
            
            # 执行视图函数获取数据
            response = view_func(request, *args, **kwargs)
            
            # 缓存响应数据
            if hasattr(response, 'status_code') and response.status_code == 200:
                cache.set(cache_key, response, timeout)
            
            return response
        return wrapper
    return decorator


def _generate_cache_key(request, prefix, user_aware, *args, **kwargs):
    """
    生成缓存键
    
    Args:
        request: 请求对象
        prefix: 键前缀
        user_aware: 是否区分用户
        *args: 位置参数
        **kwargs: 关键字参数
    
    Returns:
        str: 缓存键
    """
    # 收集影响缓存的因素
    key_parts = [prefix]
    
    # 如果需要区分用户，添加用户标识
    if user_aware:
        user_id = getattr(request.user, 'id', 'anonymous')
        key_parts.append(f"user_{user_id}")
    
    # 添加路径参数
    if args:
        key_parts.extend(str(arg) for arg in args)
    
    # 添加查询参数
    if hasattr(request, 'GET'):
        query_params = sorted(request.GET.items())
        if query_params:
            query_str = json.dumps(query_params, sort_keys=True)
            key_parts.append(hashlib.md5(query_str.encode()).hexdigest()[:8])
    
    # 添加关键字参数
    if kwargs:
        sorted_kwargs = sorted(kwargs.items())
        kwargs_str = json.dumps(sorted_kwargs, sort_keys=True)
        key_parts.append(hashlib.md5(kwargs_str.encode()).hexdigest()[:8])
    
    # 生成最终缓存键
    key_string = ":".join(key_parts)
    cache_key = hashlib.md5(key_string.encode()).hexdigest()
    
    return f"{prefix}:{cache_key}"


def invalidate_cache(pattern):
    """
    使缓存失效
    
    Args:
        pattern: 缓存键模式（支持通配符）
    
    Note:
        Redis 支持通配符删除，其他缓存后端可能需要遍历所有键
    """
    from django.core.cache import cache
    
    # 如果使用 Redis，可以使用 SCAN 命令删除匹配的键
    try:
        # 尝试获取 Redis 客户端
        if hasattr(cache, 'client'):
            client = cache.client
            # 使用 SCAN 命令查找匹配的键
            for key in client.scan_iter(match=pattern):
                cache.delete(key.decode() if isinstance(key, bytes) else key)
    except:
        # 如果不支持通配符，忽略
        pass


def cache_view_result(timeout=300, key_prefix="view"):
    """
    缓存视图函数返回结果的装饰器（简化版）
    
    适用于不需要区分用户的只读视图
    
    Args:
        timeout: 缓存过期时间（秒）
        key_prefix: 缓存键前缀
    
    Usage:
        @cache_view_result(timeout=600, key_prefix="menu")
        def get_menu_list(request):
            ...
    """
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            cache_key = f"{key_prefix}:{view_func.__name__}:{hash(str(args) + str(kwargs))}"
            
            cached_result = cache.get(cache_key)
            if cached_result is not None:
                return cached_result
            
            result = view_func(request, *args, **kwargs)
            cache.set(cache_key, result, timeout)
            
            return result
        return wrapper
    return decorator