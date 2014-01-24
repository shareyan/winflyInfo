from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()
import info.views as info
import community.views as community

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'winflyInfo.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^/',info.index),
    url(r'^getStarted$',info.getStarted),
    url(r'^manual$',info.manual),
    url(r'^community$',community.community),
    url(r'^register$',community.register),
    url(r'^login$',community.loginUser),
    url(r'^newPost$',community.newPost),
    url(r'^comment$',community.sendComment),
    url(r'^getComments$',community.getComments),
)