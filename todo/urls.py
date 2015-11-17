from django.conf.urls import patterns, url
from todo import views

urlpatterns = patterns('',
    url(r'^$', views.Home.as_view(), name='home'),
)
