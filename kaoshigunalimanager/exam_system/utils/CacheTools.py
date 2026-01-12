from django_redis import get_redis_connection


def cache_delete_pattern(pattern):
    """安全删除匹配模式的所有键"""
    conn = get_redis_connection("default")  # "default" 对应 CACHES 中的配置

    # 使用 scan_iter 替代 KEYS，避免阻塞
    deleted_count = 0
    for key in conn.scan_iter(match=pattern, count=100):  # count 每次迭代数量
        conn.delete(key)
        deleted_count += 1

    return deleted_count