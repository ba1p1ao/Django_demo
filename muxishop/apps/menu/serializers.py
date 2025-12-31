from rest_framework import serializers
from apps.menu import models


class MainMenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.MainMenu
        fields = ['main_menu_id', 'main_menu_name', 'main_menu_url']


class SubMenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.SubMenu
        fields = ['main_menu_id', 'sub_menu_id', 'sub_menu_type', 'sub_menu_name', 'sub_menu_url']