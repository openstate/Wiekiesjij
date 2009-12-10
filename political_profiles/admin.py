from django.contrib import admin

from political_profiles.models import WorkExperienceSector, PoliticalExperienceType, EducationLevel, PoliticianProfile, VisitorProfile, ChanceryProfile, ContactProfile

class EducationLevelAdmin(admin.ModelAdmin):
    pass

admin.site.register(EducationLevel, EducationLevelAdmin)

class PoliticalExperienceTypeAdmin(admin.ModelAdmin):
    pass

admin.site.register(PoliticalExperienceType, PoliticalExperienceTypeAdmin)

class WorkExperienceSectorAdmin(admin.ModelAdmin):
    pass

admin.site.register(WorkExperienceSector, WorkExperienceSectorAdmin)

class PoliticianProfileAdmin(admin.ModelAdmin):
    pass

admin.site.register(PoliticianProfile, PoliticianProfileAdmin)

class VisitorProfileAdmin(admin.ModelAdmin):
    pass
    
admin.site.register(VisitorProfile, VisitorProfileAdmin)

class ChanceryProfileAdmin(admin.ModelAdmin):
    pass

admin.site.register(ChanceryProfile, ChanceryProfileAdmin)

class ContactProfileAdmin(admin.ModelAdmin):
    pass

admin.site.register(ContactProfile, ContactProfileAdmin)