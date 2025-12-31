"""
缓存配置文件
统一管理各模块的缓存时间设置
"""

# 缓存时间配置（单位：秒）
CACHE_TIMEOUT = {
    # 商品模块
    "goods_detail": 900,      # 商品详情：15 分钟
    "goods_category": 300,    # 商品分类：5 分钟
    "goods_find": 600,        # 推荐商品：10 分钟
    "goods_search": 300,      # 商品搜索：5 分钟
    "goods_keyword": 600,     # 关键词统计：10 分钟
    
    # 菜单模块
    "main_menu": 600,         # 主菜单：10 分钟
    "sub_menu": 300,          # 子菜单：5 分钟
    
    # 购物车模块（用户相关，缓存时间较短）
    "cart": 60,               # 购物车：1 分钟
    
    # 订单模块（用户相关，缓存时间较短）
    "order": 120,             # 订单：2 分钟
    
    # 评论模块
    "comment": 300,           # 评论：5 分钟
    
    # 地址模块（用户相关）
    "address": 3600,          # 地址：1 小时
}

# 缓存键前缀配置
CACHE_KEY_PREFIX = {
    "goods": "goods",
    "menu": "menu",
    "cart": "cart",
    "order": "order",
    "comment": "comment",
    "address": "address",
}

# 是否启用缓存（可通过环境变量控制）
CACHE_ENABLED = True


def get_cache_timeout(key):
    """获取指定键的缓存时间"""
    return CACHE_TIMEOUT.get(key, 300)  # 默认 5 分钟


def get_cache_key_prefix(module):
    """获取指定模块的缓存键前缀"""
    return CACHE_KEY_PREFIX.get(module, "default")