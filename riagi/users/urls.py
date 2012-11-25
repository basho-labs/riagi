from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('riagi.users.views',
    url(r'^signup$', 'signup'),
    url(r'^logout$', 'logout'),
    url(r'^login$', 'login'),
)
