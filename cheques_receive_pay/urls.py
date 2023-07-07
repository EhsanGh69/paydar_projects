from django.urls import path

from .views import (
    ChequesList,
    ChequesCreate,
    ChequesUpdate,
    ChequesDelete,
    ChequesSearch
)



app_name = "cheques_receive_pay"


urlpatterns = [
    path('cheques/', ChequesList.as_view(), name='cheques'),
    path('cheques/search', ChequesSearch.as_view(), name='cheques_search'),
    path('cheques/create', ChequesCreate.as_view(), name='cheque_create'),
    path('cheques/update/<int:pk>', ChequesUpdate.as_view(), name='cheque_update'),
    path('cheques/delete/<int:pk>', ChequesDelete.as_view(), name='cheque_delete'),
]
