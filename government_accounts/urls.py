from django.urls import path

from .views import (
    ReceiveList, 
    ReceiveCreate, 
    ReceiveUpdate, 
    ReceiveDelete,
    ReceiveSearch,
    OrganizationList,
    OrganizationCreate,
    OrganizationUpdate,
    OrganizationDelete
)


app_name = "government_accounts"

urlpatterns = [
    path('receives/', ReceiveList.as_view(), name="receives"),
    path('receives/search', ReceiveSearch.as_view(), name="receives_search"),
    path('receives/create', ReceiveCreate.as_view(), name="receive_create"),
    path('receives/update/<int:pk>', ReceiveUpdate.as_view(), name="receive_update"),
    path('receives/delete/<int:pk>', ReceiveDelete.as_view(), name="receive_delete"),
    
    path('organizations/', OrganizationList.as_view(), name="organizations"),
    path('organizations/create', OrganizationCreate.as_view(), name="organization_create"),
    path('organizations/update/<int:pk>', OrganizationUpdate.as_view(), name="organization_update"),
    path('organizations/delete/<int:pk>', OrganizationDelete.as_view(), name="organization_delete"),
]
