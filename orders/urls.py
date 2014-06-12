from django.conf.urls import patterns, url
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = patterns('orders.views',
    url(r'^orders/$', 'order_list'),
    url(r'^orders/(?P<id>[0-9]+)$', 'order_detail'),
    url(r'^orders/(?P<order_id>[0-9]+)/(?P<product_id>[0-9]+)$',
        'ordered_item_detail'),
)

urlpatterns = format_suffix_patterns(urlpatterns)
