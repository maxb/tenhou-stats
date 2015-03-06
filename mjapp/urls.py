from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^stats/$', 'stats.views.stats_index', name='index'),
    url(r'^stats/(.*)$', 'stats.views.stats_home'),
    url(r'^$', 'mjapp.views.home'),
    url(r'^api/new_game/([^/]+)/([^/]+)', 'stats.views.api_new_game'),
    url(r'^api/new_game/([^/]+)', 'stats.views.api_new_game'),
)
