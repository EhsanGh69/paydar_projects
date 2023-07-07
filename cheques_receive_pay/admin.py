from django.contrib import admin

from .models import *



@admin.register(Cheques)
class ReceiveAdmin(admin.ModelAdmin):
    list_display = ['cheque_type', 'cheque_for', 'cheque_number', 'bank_branch', 'cheque_amount',
                    'registered', 'cheque_image', 'export_receive_date', 'due_date', 'account_owner',
                    'project', 'account_party',]
    ordering = ['-export_receive_date', 'project']
    list_filter = ['export_receive_date', 'project']
    search_fields = ['project', 'account_party']
