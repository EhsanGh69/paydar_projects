from django.contrib import admin

from .models import *



admin.site.register(Cheques)

admin.site.register(ReceivePay)

admin.site.register(Fund)

admin.site.register(CashBox)
