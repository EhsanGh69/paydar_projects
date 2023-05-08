from django.contrib import admin


from .models import *



@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['title', 'contract_type', 'owners', 'contractual_salary', 'contractual_percentage', 'costs_estimation']
    ordering = ['title']
    list_filter = ['title']
    search_fields = ['title']





