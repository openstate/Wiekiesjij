from django.conf.urls.defaults import patterns, url, include, handler500, handler404
from django.conf import settings
from django.contrib import admin


from backoffice.wizards import ElectionSetupWizard



admin.autodiscover()


urlpatterns = patterns('',
    (r'^admin/', include(admin.site.urls)),
    (r'^backoffice/', include('backoffice.urls')),
    (r'^invitation/', include('invitations.urls')),
    (r'^comments/', include('django.contrib.comments.urls')),
    (r'^opensocial/', include('opensocial.urls')),
    
    #Guessing this one should always be last
    (r'^', include('frontoffice.urls')),
)

if settings.DEBUG:
    urlpatterns += patterns('', 
        (r'', include('staticfiles.urls')),
    )
