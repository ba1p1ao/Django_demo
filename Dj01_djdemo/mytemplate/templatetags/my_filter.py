from django import template
from decimal import Decimal
# 注册过滤器
register = template.Library()


@register.filter(name="mobile_filter")  # 使用装饰器注册自定义过滤器
def mobile_filter(value, tags="****"):
    return value[:3] + tags + value[-3:]


@register.filter(name="sex_filter")
def sex_filter(value):
    return "男" if value == 1 else "女"

# 保留 n 位小数
@register.filter(name="toFixed")
def toFixed(value, n: int=2):
    """保留 n 位小数"""
    return f"{value:.{n}f}"

@register.filter(name="get_item")
def get_item(value, key):
    return value.get(key, "")
