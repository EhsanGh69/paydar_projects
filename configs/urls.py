from django.contrib import admin
from django.conf import settings
from django.urls import path, include
from django.conf.urls.static import static

from .views import index

urlpatterns = [
    path('admin/', admin.site.urls, name="home"),
    path('', index),
    path('government_accounts/', include('government_accounts.urls')),
    path('non_government_accounts/', include('non_government_accounts.urls')),
    path('projects/', include('projects.urls')),
    path('cheques_receive_pay/', include('cheques_receive_pay.urls')),
    path('account/', include('account.urls')),
]



if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
