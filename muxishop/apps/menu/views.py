from django.shortcuts import render
from django.views import View
from django.http import HttpRequest, HttpResponse, JsonResponse
from apps.menu import models
from utils.ResponseMessage import MenuResponse

class GoodsMainMenuView(View):
    def get(self, request: HttpRequest):
        menu_all = models.MainMenu.objects.all()

        print(menu_all)
        menu_list = []
        for m in menu_all:
            menu_list.append(m.__str__())

        # response_data = {
        #     "status": 200,
        #     "data": menu_list
        # }
        return MenuResponse.success(menu_list, safe=False)
    


class GoodsSubMenuView(View):
    def get(self, request: HttpRequest):
        main_menu_id = request.GET.get("main_menu_id")
        
        sub_menu = models.SubMenu.objects.filter(main_menu_id=main_menu_id)

        sub_menu_list = []
        for sm in sub_menu:
            sub_menu_list.append(sm.__str__())
        # response_data = {
        #     "status": 200,
        #     "data": sub_menu.__str__()
        # }
        return MenuResponse.success(sub_menu_list, safe=False)