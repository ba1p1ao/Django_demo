"""
缓存管理工具类
用于在数据变更时清除相关缓存
"""

from django.core.cache import cache
from utils.PageCache import invalidate_cache


class CacheManager:
    """缓存管理器"""
    
    # 缓存前缀常量
    PREFIX_GOODS = "goods"
    PREFIX_MENU = "menu"
    PREFIX_CART = "cart"
    PREFIX_ORDER = "order"
    
    @staticmethod
    def clear_goods_cache(sku_id=None):
        """
        清除商品相关缓存
        
        Args:
            sku_id: 商品SKU ID，如果为 None 则清除所有商品缓存
        """
        if sku_id:
            # 清除特定商品的缓存
            patterns = [
                f"{CacheManager.PREFIX_GOODS}_detail:*{sku_id}*",
                f"{CacheManager.PREFIX_GOODS}_category:*",
                f"{CacheManager.PREFIX_GOODS}_search:*",
            ]
        else:
            # 清除所有商品相关缓存
            patterns = [
                f"{CacheManager.PREFIX_GOODS}_detail:*",
                f"{CacheManager.PREFIX_GOODS}_category:*",
                f"{CacheManager.PREFIX_GOODS}_find:*",
                f"{CacheManager.PREFIX_GOODS}_search:*",
                f"{CacheManager.PREFIX_GOODS}_keyword:*",
            ]
        
        for pattern in patterns:
            invalidate_cache(pattern)
    
    @staticmethod
    def clear_menu_cache(main_menu_id=None):
        """
        清除菜单相关缓存
        
        Args:
            main_menu_id: 主菜单ID，如果为 None 则清除所有菜单缓存
        """
        if main_menu_id:
            patterns = [
                f"{CacheManager.PREFIX_MENU}_sub_menu:*{main_menu_id}*",
            ]
        else:
            patterns = [
                f"{CacheManager.PREFIX_MENU}_main_menu:*",
                f"{CacheManager.PREFIX_MENU}_sub_menu:*",
            ]
        
        for pattern in patterns:
            invalidate_cache(pattern)
    
    @staticmethod
    def clear_user_cache(user_id):
        """
        清除用户相关缓存（购物车、订单等）
        
        Args:
            user_id: 用户ID
        """
        patterns = [
            f"{CacheManager.PREFIX_CART}:*user_{user_id}*",
            f"{CacheManager.PREFIX_ORDER}:*user_{user_id}*",
        ]
        
        for pattern in patterns:
            invalidate_cache(pattern)
    
    @staticmethod
    def clear_all_cache():
        """
        清除所有应用缓存
        """
        patterns = [
            f"{CacheManager.PREFIX_GOODS}:*",
            f"{CacheManager.PREFIX_MENU}:*",
            f"{CacheManager.PREFIX_CART}:*",
            f"{CacheManager.PREFIX_ORDER}:*",
        ]
        
        for pattern in patterns:
            invalidate_cache(pattern)


# Django 信号处理器，用于在模型变更时自动清除缓存
def setup_cache_signals():
    """
    设置缓存信号处理器
    在 apps.py 的 ready() 方法中调用
    """
    from django.db.models.signals import post_save, post_delete
    from apps.goods.models import Goods
    from apps.menu.models import MainMenu, SubMenu
    from apps.cart.models import Cart
    from apps.order.models import Order
    
    # 商品信号处理器
    def clear_goods_on_change(sender, instance, **kwargs):
        CacheManager.clear_goods_cache(instance.sku_id if hasattr(instance, 'sku_id') else None)
    
    # 菜单信号处理器
    def clear_menu_on_change(sender, instance, **kwargs):
        if hasattr(instance, 'main_menu_id'):
            CacheManager.clear_menu_cache(instance.main_menu_id)
        else:
            CacheManager.clear_menu_cache()
    
    # 购物车信号处理器
    def clear_cart_on_change(sender, instance, **kwargs):
        if hasattr(instance, 'user_id'):
            CacheManager.clear_user_cache(instance.user_id)
    
    # 订单信号处理器
    def clear_order_on_change(sender, instance, **kwargs):
        if hasattr(instance, 'user_id'):
            CacheManager.clear_user_cache(instance.user_id)
    
    # 连接信号
    post_save.connect(clear_goods_on_change, sender=Goods)
    post_delete.connect(clear_goods_on_change, sender=Goods)
    
    post_save.connect(clear_menu_on_change, sender=MainMenu)
    post_delete.connect(clear_menu_on_change, sender=MainMenu)
    
    post_save.connect(clear_menu_on_change, sender=SubMenu)
    post_delete.connect(clear_menu_on_change, sender=SubMenu)
    
    post_save.connect(clear_cart_on_change, sender=Cart)
    post_delete.connect(clear_cart_on_change, sender=Cart)
    
    post_save.connect(clear_order_on_change, sender=Order)
    post_delete.connect(clear_order_on_change, sender=Order)