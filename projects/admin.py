from django.contrib import admin


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








