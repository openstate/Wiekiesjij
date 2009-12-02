from django.conf.urls.defaults import *

urlpatterns = patterns('',
    url('', 'invitations.views.index',name='invitations.index'),
)