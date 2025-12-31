from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from apps.menu import models, serializers
from utils.ResponseMessage import MenuResponse
from utils.PageCache import page_cache


class GoodsMainMenuView(ListAPIView):
    """获取主菜单列表"""
    serializer_class = serializers.MainMenuSerializer
    queryset = models.MainMenu.objects.all()

    @page_cache(timeout=600, key_prefix="main_menu")
    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return MenuResponse.success(serializer.data, safe=False)


class GoodsSubMenuView(APIView):
    """根据主菜单ID获取子菜单列表"""

    @page_cache(timeout=300, key_prefix="sub_menu")
    def get(self, request, *args, **kwargs):
        main_menu_id = request.GET.get("main_menu_id")

        if not main_menu_id:
            return MenuResponse.failed("缺少 main_menu_id 参数", safe=False)

        sub_menu = models.SubMenu.objects.filter(main_menu_id=main_menu_id)
        serializer = serializers.SubMenuSerializer(sub_menu, many=True)

        return MenuResponse.success(serializer.data, safe=False)