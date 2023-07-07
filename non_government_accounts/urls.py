from django.urls import path

from .views import (
    ContractorsList, 
    ContractorCreate, 
    ContractorUpdate,
    ContractorDelete, 
    ContractorSearch,
    SuppliersList,
    SupplierCreate,
    SupplierUpdate,
    SupplierDelete,
    SupplierSearch,
    PersonnelList,
    PersonnelCreate,
    PersonnelUpdate,
    PersonnelDelete,
    PersonnelSearch,
    PartnersList,
    PartnersCreate,
    PartnersUpdate,
    PartnersDelete,
    PartnerSearch,
    BuyersSellersList,
    BuyersSellersCreate,
    BuyersSellersUpdate,
    BuyersSellersDelete,
    BuyersSellersSearch,
    OrdersList,
    OrdersCreate,
    OrdersUpdate,
    OrdersDelete,
    OrdersSearch,
    ConflictOrdersList,
    ConflictOrdersCreate,
    ConflictOrdersUpdate,
    ConflictOrdersDelete,
    ConflictOrdersSearch
)


app_name = "non_government_accounts"

urlpatterns = [
    path('contractors/', ContractorsList.as_view(), name='contractors'),
    path('contractors/search', ContractorSearch.as_view(), name='contractors_search'),
    path('contractors/create', ContractorCreate.as_view(), name='contractor_create'),
    path('contractors/update/<int:pk>', ContractorUpdate.as_view(), name='contractor_update'),
    path('contractors/delete/<int:pk>', ContractorDelete.as_view(), name='contractor_delete'),

    path('suppliers/', SuppliersList.as_view(), name='suppliers'),
    path('suppliers/search', SupplierSearch.as_view(), name='suppliers_search'),
    path('suppliers/create', SupplierCreate.as_view(), name='supplier_create'),
    path('suppliers/update/<int:pk>', SupplierUpdate.as_view(), name='supplier_update'),
    path('suppliers/delete/<int:pk>', SupplierDelete.as_view(), name='supplier_delete'),

    path('personnel/', PersonnelList.as_view(), name='personnel'),
    path('personnel/search', PersonnelSearch.as_view(), name='personnel_search'),
    path('personnel/create', PersonnelCreate.as_view(), name='personnel_create'),
    path('personnel/update/<int:pk>', PersonnelUpdate.as_view(), name='personnel_update'),
    path('personnel/delete/<int:pk>', PersonnelDelete.as_view(), name='personnel_delete'),

    path('partners/', PartnersList.as_view(), name='partners'),
    path('partners/search', PartnerSearch.as_view(), name='partners_search'),
    path('partners/create', PartnersCreate.as_view(), name='partner_create'),
    path('partners/update/<int:pk>', PartnersUpdate.as_view(), name='partner_update'),
    path('partners/delete/<int:pk>', PartnersDelete.as_view(), name='partner_delete'),

    path('buyers_sellers/', BuyersSellersList.as_view(), name='buyers_sellers'),
    path('buyers_sellers/search', BuyersSellersSearch.as_view(), name='buyers_sellers_search'),
    path('buyers_sellers/create', BuyersSellersCreate.as_view(), name='buyer_seller_create'),
    path('buyers_sellers/update/<int:pk>', BuyersSellersUpdate.as_view(), name='buyer_seller_update'),
    path('buyers_sellers/delete/<int:pk>', BuyersSellersDelete.as_view(), name='buyer_seller_delete'),

    path('orders/', OrdersList.as_view(), name='orders'),
    path('orders/search', OrdersSearch.as_view(), name='orders_search'),
    path('orders/create', OrdersCreate.as_view(), name='order_create'),
    path('orders/update/<int:pk>', OrdersUpdate.as_view(), name='order_update'),
    path('orders/delete/<int:pk>', OrdersDelete.as_view(), name='order_delete'),

    path('conflict_orders/', ConflictOrdersList.as_view(), name='conflict_orders'),
    path('conflict_orders/search', ConflictOrdersSearch.as_view(), name='conflict_orders_search'),
    path('conflict_orders/create', ConflictOrdersCreate.as_view(), name='conflict_order_create'),
    path('conflict_orders/update/<int:pk>', ConflictOrdersUpdate.as_view(), name='conflict_order_update'),
    path('conflict_orders/delete/<int:pk>', ConflictOrdersDelete.as_view(), name='conflict_order_delete'),
]


