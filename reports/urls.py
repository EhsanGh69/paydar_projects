from django.urls import path

from .views import (
    ProjectReport, CostReport, WorkReferenceReport,
    ReceiveReport, PaymentReport, ActivityReport, 
    BuyerSellerReport, OrderReport, ConflictOrdersReport,
    BankReceiptReport, ConditionStatementReport,
    ChequeReport, ReceivePayReport, FundReport, CashBoxReport,
    MainWarehouseImportReport, MainWarehouseExportReport, UseCertificateReport, ProjectWarehouseReport, 
    project_stuffs_list
)


app_name = "reports"

urlpatterns = [
    path('projects/<int:pk>', ProjectReport.as_view(), name='project_report'),
    path('receives/<int:pk>', ReceiveReport.as_view(), name='receive_report'),
    path('payments/<int:pk>', PaymentReport.as_view(), name='payment_report'),
    path('activities/<int:pk>', ActivityReport.as_view(), name='activity_report'),
    path('buyers_sellers/<int:pk>', BuyerSellerReport.as_view(), name='buyer_seller_report'),
    path('orders/<int:pk>', OrderReport.as_view(), name='order_report'),
    path('costs/<int:pk>', CostReport.as_view(), name='cost_report'),
    path('work_references/<int:pk>', WorkReferenceReport.as_view(), name='work_reference_report'),
    path('conflict_orders/<int:pk>', ConflictOrdersReport.as_view(), name='conflict_order_report'),
    path('bank_receipts/<int:pk>', BankReceiptReport.as_view(), name='bank_receipt_report'),
    path('condition_statements/<int:pk>', ConditionStatementReport.as_view(), name='condition_statement_report'),
    path('cheques/<int:pk>', ChequeReport.as_view(), name='cheque_report'),
    path('receive_pays/<int:pk>', ReceivePayReport.as_view(), name='receive_pay_report'),
    path('funds/<int:pk>', FundReport.as_view(), name='fund_report'),
    path('cashboxes/<int:pk>', CashBoxReport.as_view(), name='cashbox_report'),
    path('warehouse_imports/<int:pk>', MainWarehouseImportReport.as_view(), name='warehouse_import_report'),
    path('warehouse_exports/<int:pk>', MainWarehouseExportReport.as_view(), name='warehouse_export_report'),
    path('use_certificates/<int:pk>', UseCertificateReport.as_view(), name='use_certificate_report'),
    path('project_warehouses/<int:pk>', ProjectWarehouseReport.as_view(), name='project_warehouse_report'),
    path('project_warehouses/<str:project>', project_stuffs_list, name='project_stuffs')
]
