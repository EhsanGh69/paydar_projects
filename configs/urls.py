from django.contrib import admin
from django.conf import settings
from django.urls import path, include
from django.conf.urls.static import static

from .views import index
from account.views import Login, log_out, ChangePassword

urlpatterns = [
    path('', index, name="index"),
    path('government_accounts/', include('government_accounts.urls')),
    path('non_government_accounts/', include('non_government_accounts.urls')),
    path('projects/', include('projects.urls')),
    path('cheques_receive_pay/', include('cheques_receive_pay.urls')),
    path('warehousing/', include('warehousing.urls')),
    path('projects_docs/', include('projects_docs.urls')),
    path('login/', Login.as_view(), name='login'),
    path('logout/', log_out, name='logout'),
    path('change_password/', ChangePassword.as_view(), name='change_password'),
    path('account/', include('account.urls')),
    path('reports/', include('reports.urls')),
    path('user_messages/', include('user_messages.urls')),
    path('admin/', admin.site.urls, name="home"),
]

handler404 = 'configs.views.custom_404'
handler500 = 'configs.views.custom_500'

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
