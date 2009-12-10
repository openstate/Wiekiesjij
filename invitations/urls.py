from django.conf.urls.defaults import *

urlpatterns = patterns('',
    url('^fake/$', 'invitations.views.fake', name='invitations.fake'),
    url('^(?P<hash>[a-zA-Z0-9]{32})/$', 'invitations.views.index', name='invitations.index'),
    url('^(?P<hash>[a-zA-Z0-9]{32})/accept/$', 'invitations.views.accept', name='invitations.accept'),
    url('^(?P<hash>[a-zA-Z0-9]{32})/existing/$', 'invitations.views.existing', name='invitations.existing'),
    url('notexist/$', 'invitations.views.notexist', name='invitations.notexist'),
)