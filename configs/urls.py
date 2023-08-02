from django.contrib import admin
from django.conf import settings
from django.urls import path, include
from django.conf.urls.static import static

from .views import index
from account.views import CustomLogin

urlpatterns = [
    path('', index),
    path('', include('django.contrib.auth.urls')),
    path('government_accounts/', include('government_accounts.urls')),
    path('non_government_accounts/', include('non_government_accounts.urls')),
    path('projects/', include('projects.urls')),
    path('cheques_receive_pay/', include('cheques_receive_pay.urls')),
    path('warehousing/', include('warehousing.urls')),
    path('projects_docs/', include('projects_docs.urls')),
    path('login/', CustomLogin.as_view(), name='login'),
    path('account/', include('account.urls')),
    path('admin/', admin.site.urls, name="home"),
]



if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
