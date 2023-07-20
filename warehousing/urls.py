from django.urls import path

from .views import (
    StuffList,
    StuffCreate,
    StuffUpdate,
    StuffDelete
)



app_name = 'warehousing'

urlpatterns = [
    path('stuffs/', StuffList.as_view(), name='stuffs'),
    path('stuffs/create', StuffCreate.as_view(), name='stuff_create'),
    path('stuffs/update/<int:pk>', StuffUpdate.as_view(), name='stuff_update'),
    path('stuffs/delete/<int:pk>', StuffDelete.as_view(), name='stuff_delete')
]



