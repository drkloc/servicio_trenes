from django.conf.urls.defaults import patterns, url

urlpatterns = patterns(
	'servicetrenes.views',
    url(r'^$', 'index', name='index'),
)