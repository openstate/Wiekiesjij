from django.conf.urls.defaults import *
from django.conf import settings
from django.contrib import admin


admin.autodiscover()

urlpatterns = patterns('',
    (r'^admin/', include(admin.site.urls)),
    (r'^(?P<profile_type>[-\w]+)/', 'political_profiles.views.instance_view'),
    (r'^backoffice', include('backoffice.urls')),
)


if settings.DEBUG:
    urlpatterns += patterns('', 
        (r'', include('staticfiles.urls')),
    )
