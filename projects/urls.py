from django.urls import path

from .views import (
    charts,
    OwnersList, OwnerCreate, OwnerUpdate, OwnerDelete, OwnerSearch,
    ProjectList, ProjectCreate, ProjectUpdate, ProjectDelete, ProjectSearch,
    WorkReferenceList, WorkReferenceCreate, WorkReferenceUpdate, WorkReferenceDelete, WorkReferenceSearch,
    CostsList, CostsCreate, CostsUpdate, CostsDelete, CostsSearch,
    PaymentsImagesList, PaymentsImagesCreate, PaymentsImagesUpdate, PaymentsImagesDelete, PaymentsImagesSearch
)




app_name = "projects"

urlpatterns = [
    path('charts/', charts, name='charts'),

    path('owners/', OwnersList.as_view(), name='owners'),
    path('owners/page/<int:page>', OwnersList.as_view(), name='owners'),
    path('owners/search', OwnerSearch.as_view(), name='owners_search'),
    path('owners/search/page/<int:page>', OwnerSearch.as_view(), name='owners_search'),
    path('owners/create', OwnerCreate.as_view(), name='owner_create'),
    path('owners/update/<int:pk>', OwnerUpdate.as_view(), name='owner_update'),
    path('owners/delete/<int:pk>', OwnerDelete.as_view(), name='owner_delete'),

    path('projects/', ProjectList.as_view(), name='projects'),
    path('projects/page/<int:page>', ProjectList.as_view(), name='projects'),
    path('projects/search', ProjectSearch.as_view(), name='projects_search'),
    path('projects/search/page/<int:page>', ProjectSearch.as_view(), name='projects_search'),
    path('projects/create', ProjectCreate.as_view(), name='project_create'),
    path('projects/update/<int:pk>', ProjectUpdate.as_view(), name='project_update'),
    path('projects/delete/<int:pk>', ProjectDelete.as_view(), name='project_delete'),

    path('work_references/', WorkReferenceList.as_view(), name='work_references'),
    path('work_references/page/<int:page>', WorkReferenceList.as_view(), name='work_references'),
    path('work_references/search', WorkReferenceSearch.as_view(), name='work_references_search'),
    path('work_references/search/page/<int:page>', WorkReferenceSearch.as_view(), name='work_references_search'),
    path('work_references/create', WorkReferenceCreate.as_view(), name='work_reference_create'),
    path('work_references/update/<int:pk>', WorkReferenceUpdate.as_view(), name='work_reference_update'),
    path('work_references/delete/<int:pk>', WorkReferenceDelete.as_view(), name='work_reference_delete'),

    path('costs/', CostsList.as_view(), name='costs'),
    path('costs/page/<int:page>', CostsList.as_view(), name='costs'),
    path('costs/search', CostsSearch.as_view(), name='costs_search'),
    path('costs/search/page/<int:page>', CostsSearch.as_view(), name='costs_search'),
    path('costs/create', CostsCreate.as_view(), name='cost_create'),
    path('costs/update/<int:pk>', CostsUpdate.as_view(), name='cost_update'),
    path('costs/delete/<int:pk>', CostsDelete.as_view(), name='cost_delete'),

    path('payments_images/', PaymentsImagesList.as_view(), name='payments_images'),
    path('payments_images/page/<int:page>', PaymentsImagesList.as_view(), name='payments_images'),
    path('payments_images/search', PaymentsImagesSearch.as_view(), name='payments_images_search'),
    path('payments_images/search/page/<int:page>', PaymentsImagesSearch.as_view(), name='payments_images_search'),
    path('payments_images/create', PaymentsImagesCreate.as_view(), name='payments_image_create'),
    path('payments_images/update/<int:pk>', PaymentsImagesUpdate.as_view(), name='payments_image_update'),
    path('payments_images/delete/<int:pk>', PaymentsImagesDelete.as_view(), name='payments_image_delete'),
]
