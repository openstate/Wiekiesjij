from django.conf.urls.defaults import *
from django.conf import settings
from django.contrib import admin
import backoffice.urls

admin.autodiscover()

urlpatterns = patterns('',
    (r'^admin/', include(admin.site.urls)),
    (r'^backoffice/', include('backoffice.urls')),
    (r'^invitation/', include('invitations.urls')),
    (r'^media/static/jsi18n.js', 'django.views.i18n.javascript_catalog'),
    
)

if settings.DEBUG:
    urlpatterns += patterns('', 
        (r'', include('staticfiles.urls')),
    )
