from django.urls import path
from mysession import views


app_name = "session"

urlpatterns = [
    path("get/", views.get_session),
    path("set/", views.set_session),
    path("del/", views.del_session),

]