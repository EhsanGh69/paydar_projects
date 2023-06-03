from django.urls import path

from .views import ReceiveList, ReceiveCreate


app_name = "government_accounts"

urlpatterns = [
    path('receives/', ReceiveList.as_view(), name="receives"),
    path('receives/create', ReceiveCreate.as_view(), name="receive_create")
]
