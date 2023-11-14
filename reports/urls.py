from django.urls import path

from .views import ProjectReport, ReceiveReport, PaymentReport, ActivityReport


app_name = "reports"

urlpatterns = [
    path('projects/<int:pk>', ProjectReport.as_view(), name='project_report'),
    path('receives/<int:pk>', ReceiveReport.as_view(), name='receive_report'),
    path('payments/<int:pk>', PaymentReport.as_view(), name='payment_report'),
    path('activities/<int:pk>', ActivityReport.as_view(), name='activity_report'),
]
