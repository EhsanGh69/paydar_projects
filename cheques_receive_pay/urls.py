from django.urls import path

from .views import (
    ChequesList,
    ChequesCreate,
    ChequesUpdate,
    ChequesDelete,
    ChequesSearch,
    FundList,
    fund_create,
    fund_update,
    FundSearch,
    FundDelete,
    
)



app_name = "cheques_receive_pay"


urlpatterns = [
    path('cheques/', ChequesList.as_view(), name='cheques'),
    path('cheques/search', ChequesSearch.as_view(), name='cheques_search'),
    path('cheques/create', ChequesCreate.as_view(), name='cheque_create'),
    path('cheques/update/<int:pk>', ChequesUpdate.as_view(), name='cheque_update'),
    path('cheques/delete/<int:pk>', ChequesDelete.as_view(), name='cheque_delete'),

    path('funds/', FundList.as_view(), name='funds'),
    path('funds/search', FundSearch.as_view(), name='funds_search'),
    path('funds/create', fund_create, name='fund_create'),
    path('funds/update/<int:pk>', fund_update, name='fund_update'),
    path('funds/delete/<int:pk>', FundDelete.as_view(), name='fund_delete'),
]
