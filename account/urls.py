from django.urls import path

from .views import (
    UsersList, CreateUser, UpdateUser, DeleteUser, SearchUsers,
    GroupList, CreateGroup, UpdateGroup, DeleteGroup
)

app_name = "account"

urlpatterns = [
    path('users/', UsersList.as_view(), name="users"),
    path('users/page/<int:page>', UsersList.as_view(), name="users"),
    path('users/search', SearchUsers.as_view(), name="users_search"),
    path('users/search/page/<int:page>', SearchUsers.as_view(), name="users_search"),
    path('users/create', CreateUser.as_view(), name="user_create"),
    path('users/update/<int:pk>', UpdateUser.as_view(), name="user_update"),
    path('users/delete/<int:pk>', DeleteUser.as_view(), name="user_delete"),

    path('groups/', GroupList.as_view(), name="groups"),
    path('groups/page/<int:page>', GroupList.as_view(), name="groups"),
    path('groups/create', CreateGroup.as_view(), name="group_create"),
    path('groups/update/<int:pk>', UpdateGroup.as_view(), name="group_update"),
    path('groups/delete/<int:pk>', DeleteGroup.as_view(), name="group_delete"),
] 