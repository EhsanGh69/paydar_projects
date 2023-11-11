from django.urls import path

from .views import ProjectReport, ReceiveReport


app_name = "reports"

urlpatterns = [
    path('projects/<int:pk>', ProjectReport.as_view(), name='project_report'),
    path('receives/<int:pk>', ReceiveReport.as_view(), name='receive_report'),
]
