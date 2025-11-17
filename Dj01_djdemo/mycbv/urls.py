from django.urls import path, re_path
from mycbv.views import UserListView, UserDetailView, UserByNameView

app_name = 'cbv'

urlpatterns = [
    # re_path(r"users/", UserView.as_view()),
    path("users/", UserListView.as_view()),
    path("userdetail/<int:user_id>/", UserDetailView.as_view()),
    path("users/<str:name>/", UserByNameView.as_view()),
]