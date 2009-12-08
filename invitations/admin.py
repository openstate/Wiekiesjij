from django.contrib import admin
from invitations.models import Invitation

class InvitationAdmin(admin.ModelAdmin):
    pass

admin.site.register(Invitation, InvitationAdmin)