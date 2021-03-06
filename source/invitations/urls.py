from django.conf.urls.defaults import *

urlpatterns = patterns('',
    url(r'^(?P<hash>[a-zA-Z0-9]{32})/$', 'invitations.views.index', name='invitations.index'),
    url(r'^(?P<hash>[a-zA-Z0-9]{32})/accept/$', 'invitations.views.accept', name='invitations.accept'),
    url(r'^(?P<hash>[a-zA-Z0-9]{32})/existing/$', 'invitations.views.existing', name='invitations.existing'),
    url(r'notexist/$', 'invitations.views.notexist', name='invitations.notexist'),
    
    url(r'list/$', 'invitations.views.list', name='invitations.list'),
    url(r'send/(?P<id>\d+)/$', 'invitations.views.send', name='invitations.send'),
    url(r'hijack/(?P<user_id>\d+)/$', 'invitations.views.hijack_account', name='invitations.hijack')
)