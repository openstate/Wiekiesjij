from django.contrib import admin
from invitations.models import Invitation


class InvitationAdmin(admin.ModelAdmin):
    list_display = ('user_to', 'user_from', 'type', 'hash', 'accepted', 'send_on')
    list_filter = ('type','accepted',)
    date_hierarchy = 'send_on'

admin.site.register(Invitation, InvitationAdmin)