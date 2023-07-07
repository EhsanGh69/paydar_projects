from django.contrib import admin
from jalali_date import datetime2jalali
from jalali_date.admin import ModelAdminJalaliMixin

from .models import *


@admin.register(Contractors)
class ContractorsAdmin(ModelAdminJalaliMixin, admin.ModelAdmin):
    list_display = ['project', 'full_name', 'job', 'phone']
    ordering = ['project', 'full_name']
    list_filter = ['project', 'job']
    search_fields = ['project', 'full_name']


@admin.register(Suppliers)
class ContractorsAdmin(ModelAdminJalaliMixin, admin.ModelAdmin):
    list_display = ['project', 'full_name', 'job', 'phone']
    ordering = ['project', 'full_name']
    list_filter = ['project', 'job']
    search_fields = ['project', 'full_name']


@admin.register(Personnel)
class ContractorsAdmin(ModelAdminJalaliMixin, admin.ModelAdmin):
    list_display = ['full_name', 'job', 'phone']
    ordering = ['job', 'full_name']
    list_filter = ['job', 'full_name']
    search_fields = ['job', 'full_name']


@admin.register(Partners)
class ContractorsAdmin(ModelAdminJalaliMixin, admin.ModelAdmin):
    list_display = ['investment_amount', 'project', 'full_name', 'phone']
    ordering = ['project', 'full_name']
    list_filter = ['project', 'full_name']
    search_fields = ['project', 'full_name']



@admin.register(BuyersSellers)
class BuyersSellersAdmin(ModelAdminJalaliMixin, admin.ModelAdmin):
    list_display = ['buyer_seller', 'full_name', 'phone', 'payment_order', 'payment_date', 'payment_amount']
    ordering = ['buyer_seller', 'payment_order', 'full_name']
    list_filter = ['payment_order', 'payment_date', 'buyer_seller']
    search_fields = ['payment_order', 'full_name']
    


@admin.register(Orders)
class OrdersAdmin(ModelAdminJalaliMixin, admin.ModelAdmin):
    list_display = ['supplier', 'order_type', 'measurement_unit', 'unit_price',
                    'order_amount', 'get_order_date_jalali', 'order_respite', 'order_result',
                    'get_sending_date_jalali', 'sended_image_type','explan_order_cancel',
                    'project', 'get_order_total_price'
                    ]
    ordering = ['order_date', 'supplier', 'order_type']
    list_filter = ['order_date', 'order_type']
    search_fields = ['supplier', 'order_type']

    @admin.display(description='تاریخ و ساعت سفارش', ordering='order_date')
    def get_order_date_jalali(self, obj):
        return datetime2jalali(obj.order_date).strftime('%d / %m / %Y - %H:%M:%S')
    
    @admin.display(description='تاریخ و ساعت سفارش', ordering='sending_date')
    def get_sending_date_jalali(self, obj):
        return datetime2jalali(obj.sending_date).strftime('%d / %m / %Y - %H:%M:%S')



@admin.register(ConflictOrders)
class ContractorsAdmin(ModelAdminJalaliMixin, admin.ModelAdmin):
    list_display = ['order', 'conflict_type', 'conflict_amount']
    ordering = ['conflict_type', 'order']
    list_filter = ['conflict_type']
    search_fields = ['conflict_type']






