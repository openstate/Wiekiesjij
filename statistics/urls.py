from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('statistics.views',
    url(r'^$', 'index', name='statistics.index'),
    url(r'^chartcache$', 'chart_cache', name='statistics.chartcache'),
)