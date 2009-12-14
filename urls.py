from django.conf.urls.defaults import *
from django.conf import settings
from django.contrib import admin
import backoffice.urls


from utils.graphformwizard import TestWizard
from backoffice.wizards import AddElectionInstanceWizard, ElectionSetupWizard, EditElectionInstanceWizard



admin.autodiscover()


urlpatterns = patterns('',
    (r'^admin/', include(admin.site.urls)),
    (r'^backoffice/', include('backoffice.urls')),
    (r'^invitation/', include('invitations.urls')),

    url(r'^wiz/(?P<path>[a-z0-9:]*)$', ElectionSetupWizard('test'), name = 'wizard.step'),
    url(r'^wiz/(?P<action>init)/(?P<election_instance_id>\d+)/((?P<user_id>\d+)/)?$', ElectionSetupWizard('test'), {'path':''}, name = 'wizard.elections.init'),
    url(r'^wiz/(?P<path>[a-z0-9:]*)/(?P<action>[a-zA-Z][a-zA-Z0-9_]*)$', ElectionSetupWizard('test'), name = 'wizard.action'),
)

if settings.DEBUG:
    urlpatterns += patterns('', 
        (r'', include('staticfiles.urls')),
    )
