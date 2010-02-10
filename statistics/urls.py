from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('statistics.views',
    url(r'^$', 'index',  {'tab': 'geslacht'}, name='statistics.index'),    
    url(r'^chartcache$', 'chart_cache', name='statistics.chartcache'),
    url(r'^(?P<tab>[\w-]+)/$', 'index', name='statistics.index_tab'),
)