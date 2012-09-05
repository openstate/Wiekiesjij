from django.contrib import admin

from frontoffice.models import VisitorResult


class VisitorResultAdmin(admin.ModelAdmin):
    pass

admin.site.register(VisitorResult, VisitorResultAdmin)
