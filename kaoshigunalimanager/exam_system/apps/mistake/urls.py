from django.urls import path
from apps.mistake import views

urlpatterns = [
    path("list/", views.MistakeListView.as_view())
]

