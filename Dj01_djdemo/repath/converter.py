from django.urls.converters import StringConverter, register_converter

"""自定义路由转换器"""

# 必须是以类的方式
class MobleConverter(StringConverter):
    regex = r'1[3-9]\d{9}'


# 必须要注册 converter
#register_converter(converter类名，类型名)
register_converter(MobleConverter, "moble")