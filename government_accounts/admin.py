from django.contrib import admin
from jalali_date import datetime2jalali
from jalali_date.admin import ModelAdminJalaliMixin

from .models import *



admin.site.register(Organization)


@admin.register(Receive)
class ReceiveAdmin(ModelAdminJalaliMixin, admin.ModelAdmin):
    list_display = ['organization', 'receive_for', 'project', 'receive_amount', 'get_receive_jalali']
    ordering = ['-receive_date', 'project']
    list_filter = ['receive_date', 'project', 'organization']
    search_fields = ['project', 'organization']

    @admin.display(description='تاریخ و ساعت دریافت', ordering='receive_date')
    def get_receive_jalali(self, obj):
        return datetime2jalali(obj.receive_date).strftime('%d / %m / %Y - %H:%M:%S')


@admin.register(Payment)
class ReceiveAdmin(ModelAdminJalaliMixin, admin.ModelAdmin):
    list_display = ['organization', 'payment_for', 'project', 'payment_amount', 'get_payment_jalali']
    ordering = ['-payment_date', 'project']
    list_filter = ['payment_date', 'project', 'organization']
    search_fields = ['project', 'organization']

    @admin.display(description='تاریخ و ساعت پرداخت', ordering='payment_date')
    def get_payment_jalali(self, obj):
        return datetime2jalali(obj.payment_date).strftime('%d / %m / %Y - %H:%M:%S')


@admin.register(Activity)
class ReceiveAdmin(ModelAdminJalaliMixin, admin.ModelAdmin):
    list_display = ['organization', 'activity_type', 'project', 'activity_result', 'get_activity_jalali',
                     'activity_descriptions']
    ordering = ['-activity_date', 'activity_result', 'project']
    list_filter = ['activity_date', 'project', 'organization', 'activity_result']
    search_fields = ['project', 'organization']

    @admin.display(description='تاریخ و ساعت فعالیت', ordering='activity_date')
    def get_activity_jalali(self, obj):
        return datetime2jalali(obj.activity_date).strftime('%d / %m / %Y - %H:%M:%S')




