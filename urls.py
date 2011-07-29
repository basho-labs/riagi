from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'views.home'),
    url(r'^(images|i)/', include('images.urls')),
    url(r'^users/', include('users.urls'))
)
