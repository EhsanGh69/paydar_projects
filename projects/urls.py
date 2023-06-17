from django.urls import path

from .views import (
    OwnersList, 
    OwnerCreate, 
    OwnerUpdate, 
    OwnerDelete, 
    OwnerSearch,
    OwnerImageDetail,
    ProjectList,
    ProjectCreate,
    ProjectUpdate,
    ProjectDelete,
    ProjectSearch
)




app_name = "projects"

urlpatterns = [
    path('owners/', OwnersList.as_view(), name='owners'),
    path('owners/create', OwnerCreate.as_view(), name='owner_create'),
    path('owners/search', OwnerSearch.as_view(), name='owners_search'),
    path('owners/update/<int:pk>', OwnerUpdate.as_view(), name='owner_update'),
    path('owners/delete/<int:pk>', OwnerDelete.as_view(), name='owner_delete'),
    path('owner/detail/<int:pk>', OwnerImageDetail.as_view(), name='owner_detail'),

    path('projects/', ProjectList.as_view(), name='projects'),
    path('projects/create', ProjectCreate.as_view(), name='project_create'),
    path('projects/search', ProjectSearch.as_view(), name='projects_search'),
    path('projects/update/<int:pk>', ProjectUpdate.as_view(), name='project_update'),
    path('projects/delete/<int:pk>', ProjectDelete.as_view(), name='project_delete'),
]
