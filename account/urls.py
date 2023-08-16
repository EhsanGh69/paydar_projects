from django.urls import path

from .views import UsersList, CreateUser, UpdateUser, DeleteUser, SearchUsers

app_name = "account"

urlpatterns = [
    path('users/', UsersList.as_view(), name="users"),
    path('users/search', SearchUsers.as_view(), name="users_search"),
    path('users/create', CreateUser.as_view(), name="user_create"),
    path('users/update/<int:pk>', UpdateUser.as_view(), name="user_update"),
    path('users/delete/<int:pk>', DeleteUser.as_view(), name="user_delete"),
] 