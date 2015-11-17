from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^todo/$', include('todo.urls')),
    url(r'^$', include('todo.urls', namespace='todo')),
)
