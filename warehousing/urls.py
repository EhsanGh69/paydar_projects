from django.urls import path

from .views import (
    StuffList, StuffCreate, StuffUpdate, StuffDelete, StuffSearch,
    WarehouseImportList, WarehouseImportCreate, WarehouseImportUpdate, WarehouseImportDelete, WarehouseImportSearch,
    WarehouseExportList, WarehouseExportCreate, WarehouseExportUpdate, WarehouseExportDelete, WarehouseExportSearch,
    UseCertificateList, UseCertificateCreate, UseCertificateUpdate, UseCertificateDelete, UseCertificateSearch,
    ProjectWarehouseList, ProjectWarehouseCreate, ProjectWarehouseUpdate, ProjectWarehouseDelete, ProjectWarehouseSearch
)



app_name = 'warehousing'

urlpatterns = [
    path('stuffs/', StuffList.as_view(), name='stuffs'),
    path('stuffs/page/<int:page>', StuffList.as_view(), name='stuffs'),
    path('stuffs/search', StuffSearch.as_view(), name='stuffs_search'),
    path('stuffs/search/page/<int:page>', StuffSearch.as_view(), name='stuffs_search'),
    path('stuffs/create', StuffCreate.as_view(), name='stuff_create'),
    path('stuffs/update/<int:pk>', StuffUpdate.as_view(), name='stuff_update'),
    path('stuffs/delete/<int:pk>', StuffDelete.as_view(), name='stuff_delete'),

    path('warehouse_imports/', WarehouseImportList.as_view(), name='warehouse_imports'),
    path('warehouse_imports/page/<int:page>', WarehouseImportList.as_view(), name='warehouse_imports'),
    path('warehouse_imports/search', WarehouseImportSearch.as_view(), name='warehouse_imports_search'),
    path('warehouse_imports/search/page/<int:page>', WarehouseImportSearch.as_view(), name='warehouse_imports_search'),
    path('warehouse_imports/create', WarehouseImportCreate.as_view(), name='warehouse_import_create'),
    path('warehouse_imports/update/<int:pk>', WarehouseImportUpdate.as_view(), name='warehouse_import_update'),
    path('warehouse_imports/delete/<int:pk>', WarehouseImportDelete.as_view(), name='warehouse_import_delete'),

    path('warehouse_exports/', WarehouseExportList.as_view(), name='warehouse_exports'),
    path('warehouse_exports/page/<int:page>', WarehouseExportList.as_view(), name='warehouse_exports'),
    path('warehouse_exports/search', WarehouseExportSearch.as_view(), name='warehouse_exports_search'),
    path('warehouse_exports/search/page/<int:page>', WarehouseExportSearch.as_view(), name='warehouse_exports_search'),
    path('warehouse_exports/create', WarehouseExportCreate.as_view(), name='warehouse_export_create'),
    path('warehouse_exports/update/<int:pk>', WarehouseExportUpdate.as_view(), name='warehouse_export_update'),
    path('warehouse_exports/delete/<int:pk>', WarehouseExportDelete.as_view(), name='warehouse_export_delete'),

    path('use_certificates/', UseCertificateList.as_view(), name='use_certificates'),
    path('use_certificates/page/<int:page>', UseCertificateList.as_view(), name='use_certificates'),
    path('use_certificates/search', UseCertificateSearch.as_view(), name='use_certificates_search'),
    path('use_certificates/search/page/<int:page>', UseCertificateSearch.as_view(), name='use_certificates_search'),
    path('use_certificates/create', UseCertificateCreate.as_view(), name='use_certificate_create'),
    path('use_certificates/update/<int:pk>', UseCertificateUpdate.as_view(), name='use_certificate_update'),
    path('use_certificates/delete/<int:pk>', UseCertificateDelete.as_view(), name='use_certificate_delete'),

    path('project_warehouses/', ProjectWarehouseList.as_view(), name='project_warehouses'),
    path('project_warehouses/page/<int:page>', ProjectWarehouseList.as_view(), name='project_warehouses'),
    path('project_warehouses/search', ProjectWarehouseSearch.as_view(), name='project_warehouses_search'),
    path('project_warehouses/search/page/<int:page>', ProjectWarehouseSearch.as_view(), name='project_warehouses_search'),
    path('project_warehouses/create', ProjectWarehouseCreate.as_view(), name='project_warehouse_create'),
    path('project_warehouses/update/<int:pk>', ProjectWarehouseUpdate.as_view(), name='project_warehouse_update'),
    path('project_warehouses/delete/<int:pk>', ProjectWarehouseDelete.as_view(), name='project_warehouse_delete'),
]



