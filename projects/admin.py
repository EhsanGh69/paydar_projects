from django.contrib import admin

from .models import *


admin.site.register(Owners)

admin.site.register(Project)

admin.site.register(WorkReference)

admin.site.register(Costs)

admin.site.register(PaymentsImages)
