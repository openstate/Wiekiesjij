from django.contrib import admin

from utils.models import PostLog

def user_email(obj):
    return ("%s" % obj.user.email)
    
class PostLogAdmin(admin.ModelAdmin):
    list_display = ('path', user_email, 'ipaddress', 'created', 'updated')
    search_fields = ('path', 'user__email', 'ipaddress')
    date_hierarchy = 'created'
    
    def user_email(self, obj):
          return ("%s" % (obj.user.email))
    user_email.short_description = 'User email'

admin.site.register(PostLog, PostLogAdmin)
