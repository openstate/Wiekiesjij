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
    pass
    
admin.site.register(Candidacy, CandidacyAdmin)

class ElectionInstanceModuleAdmin(admin.ModelAdmin):
    pass

admin.site.register(ElectionInstanceModule, ElectionInstanceModuleAdmin)