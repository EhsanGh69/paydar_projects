from django.urls import path

from .views import (
    StuffList,
    StuffCreate,
    StuffUpdate,
    StuffDelete,
    WarehouseImportList,
    WarehouseImportCreate,
    WarehouseImportUpdate,
    WarehouseImportDelete,
    WarehouseImportSearch
)



app_name = 'warehousing'

urlpatterns = [
    path('stuffs/', StuffList.as_view(), name='stuffs'),
    path('stuffs/create', StuffCreate.as_view(), name='stuff_create'),
    path('stuffs/update/<int:pk>', StuffUpdate.as_view(), name='stuff_update'),
    path('stuffs/delete/<int:pk>', StuffDelete.as_view(), name='stuff_delete'),

    path('warehouse_imports/', WarehouseImportList.as_view(), name='warehouse_imports'),
    path('warehouse_imports/search', WarehouseImportSearch.as_view(), name='warehouse_imports_search'),
    path('warehouse_imports/create', WarehouseImportCreate.as_view(), name='warehouse_import_create'),
    path('warehouse_imports/update/<int:pk>', WarehouseImportUpdate.as_view(), name='warehouse_import_update'),
    path('warehouse_imports/delete/<int:pk>', WarehouseImportDelete.as_view(), name='warehouse_import_delete'),
]



