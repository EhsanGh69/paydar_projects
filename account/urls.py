from django.urls import path

from .views import (
    UsersList, CreateUser, UpdateUser, DeleteUser, SearchUsers,
    GroupList, CreateGroup, UpdateGroup, DeleteGroup,
    ReportsHistory, CreateReport, ReportDelete, ReportResult, SearchReports
)

app_name = "account"

urlpatterns = [
    path('users/', UsersList.as_view(), name="users"),
    path('users/search', SearchUsers.as_view(), name="users_search"),
    path('users/create', CreateUser.as_view(), name="user_create"),
    path('users/update/<int:pk>', UpdateUser.as_view(), name="user_update"),
    path('users/delete/<int:pk>', DeleteUser.as_view(), name="user_delete"),

    path('groups/', GroupList.as_view(), name="groups"),
    path('groups/create', CreateGroup.as_view(), name="group_create"),
    path('groups/update/<int:pk>', UpdateGroup.as_view(), name="group_update"),
    path('groups/delete/<int:pk>', DeleteGroup.as_view(), name="group_delete"),

    path('reports/', ReportsHistory.as_view(), name="reports"),
    path('reports/search', SearchReports.as_view(), name="reports_search"),
    path('reports/create', CreateReport.as_view(), name="report_create"),
    path('reports/result/<int:pk>', ReportResult.as_view(), name="report_result"),
    path('reports/delete/<int:pk>', ReportDelete.as_view(), name="report_delete"),
] 