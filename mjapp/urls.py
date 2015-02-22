from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^stats/$', 'stats.views.stats_home'),
    url(r'^$', 'mjapp.views.home'),
)
