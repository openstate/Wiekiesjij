from django.contrib import admin

from elections.models import Council, ElectionEvent, ElectionInstance, ElectionInstanceQuestion, ElectionInstanceQuestionAnswer, ElectionInstanceParty, Party, Candidacy, ElectionInstanceModule

class CouncilAdmin(admin.ModelAdmin):
    pass

admin.site.register(Council, CouncilAdmin)

class ElectionEventAdmin(admin.ModelAdmin):
    pass

admin.site.register(ElectionEvent, ElectionEventAdmin)

class ElectionInstanceAdmin(admin.ModelAdmin):
    pass

admin.site.register(ElectionInstance, ElectionInstanceAdmin)

class ElectionInstancePartyAdmin(admin.ModelAdmin):
    pass

admin.site.register(ElectionInstanceParty, ElectionInstancePartyAdmin)

class ElectionInstanceQuestionAdmin(admin.ModelAdmin):
    list_display = ('question', 'position',)

admin.site.register(ElectionInstanceQuestion, ElectionInstanceQuestionAdmin)

class ElectionInstanceQuestionAnswerAdmin(admin.ModelAdmin):
    pass

admin.site.register(ElectionInstanceQuestionAnswer, ElectionInstanceQuestionAnswerAdmin)

class PartyAdmin(admin.ModelAdmin):
    pass

admin.site.register(Party, PartyAdmin)


class CandidacyAdmin(admin.ModelAdmin):
    list_display = ('candidate_name', 'election_party_instance', 'position', 'elected')
    list_filter = ('election_party_instance', )
    actions = ['mark_elected', 'mark_not_elected']


    # Yes, this is inefficient. Fixit.
    def candidate_name(self,obj):
        return "%s %s" % (obj.candidate.profile.first_name, obj.candidate.profile.last_name)

    def mark_elected(self, request, queryset):
        queryset.update(elected=True)

    def mark_not_elected(self, request, queryset):
        queryset.update(elected=False)

admin.site.register(Candidacy, CandidacyAdmin)

class ElectionInstanceModuleAdmin(admin.ModelAdmin):
    pass

admin.site.register(ElectionInstanceModule, ElectionInstanceModuleAdmin)
