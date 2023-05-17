from django.contrib import admin
from jalali_date import datetime2jalali
from jalali_date.admin import ModelAdminJalaliMixin

from .models import *


@admin.register(Contractors)
class ContractorsAdmin(ModelAdminJalaliMixin, admin.ModelAdmin):
    list_display = ['project', 'firstname', 'lastname', 'job', 'phone']
    ordering = ['project', 'lastname']
    list_filter = ['project', 'job']
    search_fields = ['project', 'lastname']


@admin.register(Suppliers)
class ContractorsAdmin(ModelAdminJalaliMixin, admin.ModelAdmin):
    list_display = ['project', 'firstname', 'lastname', 'job', 'phone']
    ordering = ['project', 'lastname']
    list_filter = ['project', 'job']
    search_fields = ['project', 'lastname']


@admin.register(Personnel)
class ContractorsAdmin(ModelAdminJalaliMixin, admin.ModelAdmin):
    list_display = ['firstname', 'lastname', 'job', 'phone', 'contract_tag']
    ordering = ['job', 'lastname']
    list_filter = ['job', 'lastname']
    search_fields = ['job', 'lastname']


@admin.register(Partners)
class ContractorsAdmin(ModelAdminJalaliMixin, admin.ModelAdmin):
    list_display = ['investment_amount', 'project', 'contract_tag', 'full_name', 'phone']
    ordering = ['project', 'full_name']
    list_filter = ['project', 'full_name']
    search_fields = ['project', 'full_name']








