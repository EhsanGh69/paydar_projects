from django.contrib import admin

from .models import *


admin.site.register(Contractors)

admin.site.register(Suppliers)

admin.site.register(Personnel)

admin.site.register(Partners)

admin.site.register(BuyersSellers)

admin.site.register(Orders)

admin.site.register(ConflictOrders)
