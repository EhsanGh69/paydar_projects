from django.urls import path

from .views import (
    ChequesList,
    ChequesCreate,
    ChequesUpdate,
    ChequesDelete,
    ChequesSearch,
    FundList,
    FundCreate,
    FundUpdate,
    FundSearch,
    FundDelete,
    ReceivePayList,
    ReceivePayCreate,
    ReceivePayUpdate,
    ReceivePayDelete,
    ReceivePaySearch,
    CashBoxList,
    cash_box_create,
    cash_box_update,
    CashBoxDelete,
    CashBoxSearch
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
    path('funds/create', FundCreate.as_view(), name='fund_create'),
    path('funds/update/<int:pk>', FundUpdate.as_view(), name='fund_update'),
    path('funds/delete/<int:pk>', FundDelete.as_view(), name='fund_delete'),

    path('cash_boxes/', CashBoxList.as_view(), name='cash_boxes'),
    path('cash_boxes/search', CashBoxSearch.as_view(), name='cash_boxes_search'),
    path('cash_boxes/create', cash_box_create, name='cash_box_create'),
    path('cash_boxes/update/<int:pk>', cash_box_update, name='cash_box_update'),
    path('cash_boxes/delete/<int:pk>', CashBoxDelete.as_view(), name='cash_box_delete'),
]
