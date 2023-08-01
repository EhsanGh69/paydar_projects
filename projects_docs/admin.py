from django.contrib import admin

from .models import *


admin.site.register(Contracts)

admin.site.register(Proceedings)

admin.site.register(Agreements)

admin.site.register(BankReceipts)

admin.site.register(ConditionStatements)

admin.site.register(RegisteredDocs)

admin.site.register(OfficialDocs)
