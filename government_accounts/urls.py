from django.urls import path

from .views import ReceiveList, ReceiveCreate, ReceiveUpdate, ReceiveDelete


app_name = "government_accounts"

urlpatterns = [
    path('receives/', ReceiveList.as_view(), name="receives"),
    path('receives/create', ReceiveCreate.as_view(), name="receive_create"),
    path('receives/update/<int:pk>', ReceiveUpdate.as_view(), name="receive_update"),
    path('receives/delete/<int:pk>', ReceiveDelete.as_view(), name="receive_delete"),
]
