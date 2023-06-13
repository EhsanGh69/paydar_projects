from django.urls import path

from .views import OwnersList, OwnerCreate, OwnerUpdate, OwnerDelete, OwnerSearch




app_name = "projects"

urlpatterns = [
    path('owners/', OwnersList.as_view(), name='owners'),
    path('owners/create', OwnerCreate.as_view(), name='owner_create'),
    path('owners/search', OwnerSearch.as_view(), name='owners_search'),
    path('owners/update/<int:pk>', OwnerUpdate.as_view(), name='owner_update'),
    path('owners/delete/<int:pk>', OwnerDelete.as_view(), name='owner_delete'),
]
