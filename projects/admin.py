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
class WorkReferenceAdmin(ModelAdminJalaliMixin, admin.ModelAdmin):
    list_display = ['project', 'activity_type', 'referrer', 'doing_agent', 'follow_confirm', 'get_follow_date_jalali']
    ordering = ['project', 'activity_type']
    list_filter = ['project', 'activity_type', 'follow_date']
    search_fields = ['project', 'activity_type', 'referrer', 'doing_agent']

    @admin.display(description='تاریخ و ساعت پیگیری', ordering='follow_date')
    def get_follow_date_jalali(self, obj):
        return datetime2jalali(obj.follow_date).strftime('%d / %m / %Y - %H:%M:%S')
    

@admin.register(Costs)
class CostsAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {"fields": 
                    ("project", )
                }
        ),
        ("هزینه انشعابات", {"fields": 
                                ("water_branch", "electricity_branch", "gas_branch", "phone_subscription")
                            }
        ),
        ("هزینه های نظام مهندسی", {"fields": 
                                ("designer_office", "supervisors", "engineer_system", "sketch_map")
                            }
        ),
        ("هزینه های شهرداری", {"fields": 
                                ("export_permit", "export_end_work")
                            }
        )
    )
    list_display = ['project',
                    "water_branch", "electricity_branch", "gas_branch", "phone_subscription",
                    "designer_office", "supervisors", "engineer_system", "sketch_map",
                    "export_permit", "export_end_work"
                    ]
    ordering = ['project']
    list_filter = ['project']
    search_fields = ['project']


@admin.register(ImagesPaymentReceipts)
class ImagesPaymentReceiptsAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {"fields": 
                    ("project", )
                }
        ),
        ("تصاویر فیش های پرداختی نظام مهندسی", {"fields": 
                                ("designer_office", "supervisors", "engineer_system", "sketch_map")
                            }
        ),
        ("تصاویر فیش های پرداختی شهرداری", {"fields": 
                                ("export_permit", "visit_toll", "education_share", 
                                 "fire_stations_share","social_security_share")
                            }
        )
    )
    list_display = ['project',
                    "designer_office_tag", "supervisors_tag", "engineer_system_tag", "sketch_map_tag",
                    "export_permit_tag", "visit_toll_tag", "education_share_tag", 
                    "fire_stations_share_tag","social_security_share_tag"
                    ]
    ordering = ['project']
    list_filter = ['project']
    search_fields = ['project']








