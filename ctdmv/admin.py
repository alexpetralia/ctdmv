from django.contrib import admin

from ctdmv.models import (Service, Branch, WaitEntry)

admin.site.register(Service)
admin.site.register(Branch)
admin.site.register(WaitEntry)
