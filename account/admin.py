from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group
from .models import User


admin.site.site_header = "پروژه‌های پایدار"
admin.site.site_title = "مدیریت سایت"
admin.site.index_title = "پروژه‌های پایدار"

admin.site.register(User, UserAdmin)
admin.site.unregister(Group)
