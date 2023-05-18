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



@admin.register(BuyersSellers)
class BuyersSellersAdmin(ModelAdminJalaliMixin, admin.ModelAdmin):
    list_display = ['buyer_seller', 'full_name', 'phone', 'contract_tag',
                    'payment_order', 'get_buyers_sellers_jalali', 'cash_amount',
                    'cheque_payment', 'delivery_amount', 'delivery_cheque',
                    'doc_transfer_amount', 'doc_transfer_cheque'
                    ]
    ordering = ['buyer_seller', 'payment_order', 'full_name']
    list_filter = ['payment_order', 'full_name']
    search_fields = ['payment_order', 'full_name']

    @admin.display(description='تاریخ و ساعت پرداخت نقدی', ordering='cash_date')
    def get_buyers_sellers_jalali(self, obj):
        return datetime2jalali(obj.cash_date).strftime('%d / %m / %Y - %H:%M:%S')








