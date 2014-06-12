from django.conf.urls import patterns, url
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = patterns('products.views',
    url(r'^products/$', 'product_list'),
    url(r'^products/(?P<id>[0-9]+)$', 'product_detail'),
)

urlpatterns = format_suffix_patterns(urlpatterns)
