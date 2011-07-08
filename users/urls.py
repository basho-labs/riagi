from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('users.views',
    url(r'^signup$', 'signup')
)
