from django.contrib import admin

from .models import *


admin.site.register(Organization)

admin.site.register(Receive)

admin.site.register(Payment)

admin.site.register(Activity)
