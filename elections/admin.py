from django.contrib import admin

from elections.models import Council, ElectionEvent, ElectionInstance, ElectionInstanceQuestion, ElectionInstanceParty, Party, Candidacy

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
    pass

admin.site.register(ElectionInstanceQuestion, ElectionInstanceQuestionAdmin)

class PartyAdmin(admin.ModelAdmin):
    pass

admin.site.register(Party, PartyAdmin)

class CandidacyAdmin(admin.ModelAdmin):
    pass
    
admin.site.register(Candidacy, CandidacyAdmin)

