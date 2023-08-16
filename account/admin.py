from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


admin.site.site_header = "پروژه‌های پایدار"
admin.site.site_title = "مدیریت سایت"
admin.site.index_title = "پروژه‌های پایدار"

UserAdmin.fieldsets[2][1]["fields"] = (
    "is_active",
    "is_staff",
    "is_superuser",
    "groups",
    "mobile_number",
    "user_permissions",
)

UserAdmin.list_display += ("mobile_number",) # type: ignore

admin.site.register(User, UserAdmin)

