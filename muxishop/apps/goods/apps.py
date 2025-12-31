from django.apps import AppConfig


class GoodsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.goods'

    def ready(self):
        """应用启动时设置缓存信号处理器"""
        try:
            from utils.CacheManager import setup_cache_signals
            setup_cache_signals()
        except ImportError:
            pass
