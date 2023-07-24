from django.contrib import admin

from .models import *



admin.site.register(Stuff)

admin.site.register(MainWarehouseImport)

admin.site.register(MainWarehouseExport)

admin.site.register(UseCertificate)

admin.site.register(ProjectWarehouse)
