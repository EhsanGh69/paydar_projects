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
    ReceivePayList,
    ReceivePayCreate,
    ReceivePayUpdate,
    ReceivePayDelete,
    ReceivePaySearch
)



app_name = "cheques_receive_pay"


urlpatterns = [
    path('cheques/', ChequesList.as_view(), name='cheques'),
    path('cheques/search', ChequesSearch.as_view(), name='cheques_search'),
    path('cheques/create', ChequesCreate.as_view(), name='cheque_create'),
    path('cheques/update/<int:pk>', ChequesUpdate.as_view(), name='cheque_update'),
    path('cheques/delete/<int:pk>', ChequesDelete.as_view(), name='cheque_delete'),

    path('receive_pays/', ReceivePayList.as_view(), name='receive_pays'),
    path('receive_pays/search', ReceivePaySearch.as_view(), name='receive_pays_search'),
    path('receive_pays/create', ReceivePayCreate.as_view(), name='receive_pay_create'),
    path('receive_pays/update/<int:pk>', ReceivePayUpdate.as_view(), name='receive_pay_update'),
    path('receive_pays/delete/<int:pk>', ReceivePayDelete.as_view(), name='receive_pay_delete'),

    path('funds/', FundList.as_view(), name='funds'),
    path('funds/search', FundSearch.as_view(), name='funds_search'),
    path('funds/create', fund_create, name='fund_create'),
    path('funds/update/<int:pk>', fund_update, name='fund_update'),
    path('funds/delete/<int:pk>', FundDelete.as_view(), name='fund_delete'),
]
