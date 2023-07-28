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
    WarehouseImportSearch,
    WarehouseExportList,
    WarehouseExportCreate,
    WarehouseExportUpdate,
    WarehouseExportDelete,
    WarehouseExportSearch,
    UseCertificateList,
    UseCertificateCreate,
    UseCertificateUpdate,
    UseCertificateDelete,
    UseCertificateSearch
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

    path('warehouse_exports/', WarehouseExportList.as_view(), name='warehouse_exports'),
    path('warehouse_exports/search', WarehouseExportSearch.as_view(), name='warehouse_exports_search'),
    path('warehouse_exports/create', WarehouseExportCreate.as_view(), name='warehouse_export_create'),
    path('warehouse_exports/update/<int:pk>', WarehouseExportUpdate.as_view(), name='warehouse_export_update'),
    path('warehouse_exports/delete/<int:pk>', WarehouseExportDelete.as_view(), name='warehouse_export_delete'),

    path('use_certificates/', UseCertificateList.as_view(), name='use_certificates'),
    path('use_certificates/search', UseCertificateSearch.as_view(), name='use_certificates_search'),
    path('use_certificates/create', UseCertificateCreate.as_view(), name='use_certificate_create'),
    path('use_certificates/update/<int:pk>', UseCertificateUpdate.as_view(), name='use_certificate_update'),
    path('use_certificates/delete/<int:pk>', UseCertificateDelete.as_view(), name='use_certificate_delete'),
]



