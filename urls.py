from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'riagi.views.home'),
    url(r'^(images|i)/', include('images.urls')),
    url(r'^users/', include('users.urls'))
)
