from django.conf.urls.defaults import *

urlpatterns = patterns('',
    url('^$', 'invitations.views.index',name='invitations.index'),
    url(r'^sent/$', 'invitations.views.sent'),
    url(r'^activate/(?P<hash>[a-zA-Z0-9]+)/$', 'invitations.views.activate'),
)