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
    OrganizationDelete,
    PaymentList,
    PaymentCreate,
    PaymentUpdate,
    PaymentDelete,
    PaymentSearch,
    ActivityList,
    ActivityCreate,
    ActivityUpdate,
    ActivityDelete,
    ActivitySearch
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

    path('payments/', PaymentList.as_view(), name="payments"),
    path('payments/search', PaymentSearch.as_view(), name="payments_search"),
    path('payments/create', PaymentCreate.as_view(), name="payment_create"),
    path('payments/update/<int:pk>', PaymentUpdate.as_view(), name="payment_update"),
    path('payments/delete/<int:pk>', PaymentDelete.as_view(), name="payment_delete"),

    path('activities/', ActivityList.as_view(), name="activities"),
    path('activities/search', ActivitySearch.as_view(), name="activities_search"),
    path('activities/create', ActivityCreate.as_view(), name="activity_create"),
    path('activities/update/<int:pk>', ActivityUpdate.as_view(), name="activity_update"),
    path('activities/delete/<int:pk>', ActivityDelete.as_view(), name="activity_delete"),
]
