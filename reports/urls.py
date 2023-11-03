from django.urls import path

from .views import ProjectReport


app_name = "reports"

urlpatterns = [
    path('projects/<int:pk>', ProjectReport.as_view(), name='project_report')
]
