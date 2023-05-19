from django.contrib import admin
from jalali_date import datetime2jalali
from jalali_date.admin import ModelAdminJalaliMixin


from .models import *


@admin.register(Owners)
class OwnersAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'phone', 'national_card_tag', 'birth_certificate_tag', 'ownership_document_tag']
    ordering = ['full_name']
    list_filter = ['full_name']
    search_fields = ['full_name']



@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['title', 'contract_type', 'owners_to_str', 'contractual_salary', 'contractual_percentage', 'costs_estimation']
    ordering = ['title']
    list_filter = ['title']
    search_fields = ['title']


@admin.register(WorkReference)
class ReceiveAdmin(ModelAdminJalaliMixin, admin.ModelAdmin):
    list_display = ['project', 'activity_type', 'referrer', 'doing_agent', 'follow_confirm', 'get_follow_date_jalali']
    ordering = ['project', 'activity_type']
    list_filter = ['project', 'activity_type', 'follow_date']
    search_fields = ['project', 'activity_type', 'referrer', 'doing_agent']

    @admin.display(description='تاریخ و ساعت پیگیری', ordering='follow_date')
    def get_follow_date_jalali(self, obj):
        return datetime2jalali(obj.follow_date).strftime('%d / %m / %Y - %H:%M:%S')








