from django.urls import path

from .views import (
    ContractsList,
    ContractsCreate,
    ContractsUpdate,
    ContractsDelete,
    ContractsSearch
)



app_name = 'projects_docs'


urlpatterns = [
    path('contracts/', ContractsList.as_view(), name='contracts'),
    path('contracts/search', ContractsSearch.as_view(), name='contracts_search'),
    path('contracts/create', ContractsCreate.as_view(), name='contract_create'),
    path('contracts/update/<int:pk>', ContractsUpdate.as_view(), name='contract_update'),
    path('contracts/delete/<int:pk>', ContractsDelete.as_view(), name='contract_delete'),
]




