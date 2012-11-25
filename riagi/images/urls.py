from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('riagi.images.views',
    url(r'^upload$', 'upload'),
    url(r'^(?P<image_id>[a-zA-Z0-9]{5,6})$', 'show'),
    url(r'^(?P<image_id>[a-zA-Z0-9]{5,6})\.[a-z]{3}$', 'fetch'),
    url(r'^t/(?P<image_id>[a-zA-Z0-9]{5,6})\.[a-z]{3}$', 'fetch',
        {"thumb": True}),
    url(r'^mine$', 'mine')
)
