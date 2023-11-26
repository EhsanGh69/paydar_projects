from django.urls import path

from .views import (
    ProjectReport, CostReport, WorkReferenceReport,
    ReceiveReport, PaymentReport, ActivityReport, 
    BuyerSellerReport, OrderReport
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
    path('work_reference/<int:pk>', WorkReferenceReport.as_view(), name='work_reference_report'),
]
