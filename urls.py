from django.conf.urls import include, url
from django.contrib import admin

from . import views

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^stats/$', views.stats_index, name='index'),
    url(r'^stats/(.*)$', views.stats_home),
    url(r'^stats_markdown/(.*)$', views.stats_markdown),
    url(r'^game/(.*)$', views.stats_game),
    url(r'^$', views.home),
    url(r'^api/new_game/([^/]+)/([^/]+)', views.api_new_game),
    url(r'^api/new_game/([^/]+)', views.api_new_game),
]
