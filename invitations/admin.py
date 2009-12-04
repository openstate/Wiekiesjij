from django.contrib import admin
from invitations.models import CandidateInvitation

class CandidateInvitationAdmin(admin.ModelAdmin):
    pass

admin.site.register(CandidateInvitation, CandidateInvitationAdmin)