from django.contrib import admin

from political_profiles.models import PoliticianProfile, VisitorProfile, ChanceryProfile, ContactProfile


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