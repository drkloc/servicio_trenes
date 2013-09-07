from django.conf.urls.defaults import patterns, include, url

from socketio import sdjango

from django.contrib import admin

admin.autodiscover()
sdjango.autodiscover()


urlpatterns = patterns('views',
    url(r'^$', 'index', name='index'),
)


urlpatterns += patterns('',
    url("^socket\.io", include(sdjango.urls)),
    url(r'^admin/', include(admin.site.urls)),
)
